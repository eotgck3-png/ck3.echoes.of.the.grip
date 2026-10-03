// Run PX Toolkit's language server headless and print its diagnostics for mod files.
//
// PX Toolkit (VS Code extension jdeffner.px-toolkit) ships its analysis as an LSP server
// (dist/server.js, "px-lsp"). This opens every .txt / .yml under the given paths in that
// server, the way VS Code would, and collects what it publishes: structural problems,
// loc-file problems (BOM, header, bad entries), unknown or undefined references, scope
// mismatches. Complements Tiger and docs/tools/px_vocab_check.py.
//
// Node is not on PATH here; VS Code's own runtime is used instead:
//   ELECTRON_RUN_AS_NODE=1 "/c/Users/river/AppData/Local/Programs/Microsoft VS Code/Code.exe" \
//     docs/tools/px_lsp_diagnostics.js common events localization
// Options: --verbose (server log to stderr), --quiet-ms=N (settle time, default 8000).
// Exit status 1 when any error or warning is reported.

const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL, fileURLToPath } = require("url");

const GAME = "D:/SteamLibrary/steamapps/common/Crusader Kings III/game";
const MOD = path.resolve(__dirname, "..", "..");
const args = process.argv.slice(2);
const verbose = args.includes("--verbose");
const quietMs = Number((args.find((a) => a.startsWith("--quiet-ms=")) || "=8000").split("=")[1]);
const targets = args.filter((a) => !a.startsWith("--"));
const requests = args.filter((a) => a.startsWith("--request=")).map((a) => a.split("=")[1]);
const outDir = (args.find((a) => a.startsWith("--out=")) || "=" + os.tmpdir()).split("=").slice(1).join("=");
if (!targets.length) {
  console.error("usage: px_lsp_diagnostics.js <file-or-dir> [...] [--verbose] [--quiet-ms=N]");
  process.exit(2);
}

const extDir = path.join(os.homedir(), ".vscode", "extensions");
const pxDir = fs.readdirSync(extDir).filter((d) => d.startsWith("jdeffner.px-toolkit-")).sort().pop();
if (!pxDir) {
  console.error("PX Toolkit not found under " + extDir);
  process.exit(2);
}
const serverJs = path.join(extDir, pxDir, "dist", "server.js");

function collect(p, out) {
  const st = fs.statSync(p);
  if (st.isDirectory()) for (const e of fs.readdirSync(p)) collect(path.join(p, e), out);
  else if (/\.(txt|yml)$/i.test(p)) out.push(path.resolve(p));
  return out;
}
const files = targets.flatMap((t) => collect(path.resolve(MOD, t), []));

const settings = { gamePath: GAME, gameId: "ck3", locLanguage: "english", modPath: MOD };
const server = spawn(process.execPath, [serverJs, "--stdio"], {
  env: { ...process.env, ELECTRON_RUN_AS_NODE: "1" },
  stdio: ["pipe", "pipe", verbose ? "inherit" : "ignore"],
});

let nextId = 1;
const pending = new Map();
function send(msg) {
  const body = JSON.stringify({ jsonrpc: "2.0", ...msg });
  server.stdin.write(`Content-Length: ${Buffer.byteLength(body)}\r\n\r\n${body}`);
}
function request(method, params) {
  const id = nextId++;
  send({ id, method, params });
  return new Promise((resolve) => pending.set(id, resolve));
}

const diagnostics = new Map();
let lastActivity = Date.now();
// Diagnostics published before indexing finishes miss every vanilla definition (they
// report vanilla loc keys as missing, etc.). The server announces the end of indexing
// with the custom notification paradox/progress { phase: "index", state: "done" }.
let indexed = false;

function onMessage(msg) {
  if (msg.id !== undefined && msg.method === undefined) {
    const r = pending.get(msg.id);
    if (r) { pending.delete(msg.id); r(msg.result); }
    return;
  }
  if (msg.id !== undefined) {
    // Server-to-client request: answer so the server never stalls.
    let result = null;
    if (msg.method === "workspace/configuration") result = (msg.params.items || []).map(() => settings);
    else if (msg.method === "workspace/workspaceFolders") result = [{ uri: pathToFileURL(MOD).href, name: "mod" }];
    send({ id: msg.id, result });
    return;
  }
  if (msg.method === "textDocument/publishDiagnostics") {
    diagnostics.set(msg.params.uri, msg.params.diagnostics);
    lastActivity = Date.now();
  } else if (msg.method === "paradox/progress") {
    if (msg.params.phase === "index" && msg.params.state === "done") indexed = true;
    lastActivity = Date.now();
  } else if (verbose && msg.method === "window/logMessage") {
    process.stderr.write(`[px] ${msg.params.message}\n`);
  }
}

let buf = Buffer.alloc(0);
server.stdout.on("data", (chunk) => {
  buf = Buffer.concat([buf, chunk]);
  for (;;) {
    const sep = buf.indexOf("\r\n\r\n");
    if (sep < 0) return;
    const len = Number(/Content-Length: (\d+)/i.exec(buf.slice(0, sep).toString())[1]);
    if (buf.length < sep + 4 + len) return;
    const body = buf.slice(sep + 4, sep + 4 + len).toString("utf8");
    buf = buf.slice(sep + 4 + len);
    onMessage(JSON.parse(body));
  }
});

const SEV = { 1: "error", 2: "warning", 3: "info", 4: "hint" };

(async () => {
  const root = pathToFileURL(MOD).href;
  await request("initialize", {
    processId: process.pid,
    rootUri: root,
    workspaceFolders: [{ uri: root, name: "mod" }],
    capabilities: { workspace: { configuration: true, workspaceFolders: true }, textDocument: { publishDiagnostics: {} } },
    initializationOptions: { settings },
  });
  send({ method: "initialized", params: {} });
  for (const f of files) {
    send({
      method: "textDocument/didOpen",
      params: {
        textDocument: {
          uri: pathToFileURL(f).href,
          languageId: /\.yml$/i.test(f) ? "paradox-loc" : "paradox-ck3",
          version: 1,
          text: fs.readFileSync(f, "utf8"),
        },
      },
    });
  }
  lastActivity = Date.now();
  // Wait for indexing to finish, then for diagnostics to settle (capped at 10 minutes).
  const start = Date.now();
  while ((!indexed || Date.now() - lastActivity < quietMs) && Date.now() - start < 600000) {
    await new Promise((r) => setTimeout(r, 500));
  }
  if (!indexed) console.log("!! PX never reported indexing complete; results may lack vanilla definitions");
  let problems = 0, shown = 0;
  for (const [uri, list] of [...diagnostics].sort()) {
    const rel = path.relative(MOD, fileURLToPath(uri)).replace(/\\/g, "/");
    for (const d of list) {
      const sev = SEV[d.severity] || "info";
      if (sev === "error" || sev === "warning") problems++;
      shown++;
      const code = d.code !== undefined ? ` [${d.code}]` : "";
      console.log(`${rel}:${d.range.start.line + 1}:${d.range.start.character + 1}: ${sev}${code} ${d.message.replace(/\s+/g, " ")}`);
    }
  }
  console.log(`-- ${files.length} files, ${diagnostics.size} reported, ${shown} diagnostics, ${problems} errors/warnings (${pxDir})`);
  for (const name of requests) {
    const result = await request(`paradox/${name}`, { modRoot: MOD });
    const out = path.join(outDir, `px_${name}.json`);
    fs.writeFileSync(out, JSON.stringify(result, null, 1));
    console.log(`-- paradox/${name} -> ${out}`);
  }
  await request("shutdown", null);
  send({ method: "exit" });
  process.exit(problems ? 1 : 0);
})();
