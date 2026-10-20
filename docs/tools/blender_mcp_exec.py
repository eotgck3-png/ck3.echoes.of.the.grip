"""Run a Python file inside a live Blender through the MCP addon's socket.

The `blender` MCP server in C:/Users/river/MCP/.mcp.json (mcp-for-blender) is a thin client for
the addon's TCP server on localhost:9876, and it only attaches to sessions started in that
workspace. This speaks the same protocol directly, so a session in this repo can drive the same
Blender: one JSON command, {"type": "execute_code", "params": {"code": ...}}, one JSON reply.

Blender must be running with the addon's server started (it auto-starts in the GUI).

Usage:
    python docs/tools/blender_mcp_exec.py <file.py> [--call "build(r'C:/mod', render=True)"]
    python docs/tools/blender_mcp_exec.py --code "print(len(bpy.data.objects))"
"""
from __future__ import annotations

import argparse
import json
import socket
import sys


def send(code, host="localhost", port=9876, timeout=1800):
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall(json.dumps({"type": "execute_code", "params": {"code": code}}).encode("utf-8"))
        buf = b""
        while True:
            chunk = s.recv(1 << 16)
            if not chunk:
                break
            buf += chunk
            try:
                return json.loads(buf.decode("utf-8"))
            except ValueError:
                continue
    return json.loads(buf.decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--call", default="")
    ap.add_argument("--code", default="")
    ap.add_argument("--port", type=int, default=9876)
    a = ap.parse_args()
    code = open(a.file, encoding="utf-8").read() if a.file else ""
    code += "\n" + a.call + "\n" + a.code + "\n"
    reply = send(code, port=a.port)
    if reply.get("status") == "error":
        msg = reply.get("message", "")
        try:
            msg = json.loads(msg).get("traceback", msg)
        except ValueError:
            pass
        print(msg)
        sys.exit(1)
    print(reply.get("result", {}).get("result", reply))


if __name__ == "__main__":
    main()
