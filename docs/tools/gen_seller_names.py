"""Generate the cybernetics seller-name files from the owner's list (CB-42).

    python docs/tools/gen_seller_names.py [--root CHECKOUT] [--check]

Reads cybernetics_seller_names.txt at the root of the checkout ([companies], [gangs],
[syndicates]), validates every name (docs/specs/cybernetics_v2_seller_names.md §4.2,
§8.3), and writes three files:

  common/customizable_localization/eotg_aug_seller_names.txt   custom loc (one text per
      name, read from a character variable holding a flag; plus a fallback text)
  common/scripted_effects/eotg_aug_seller_roll_effects.txt     the roll effects
  localization/english/eotg_aug_seller_names_l_english.yml     the name and fallback keys

The name rules are data in docs/tools/eotg_lint_register.json: every L012 "error" rule
plus "name_never" and "name_banned_words" for companies and gangs; "syndicate_never"
(reject) and "syndicate_warn" (print, exit 0) for syndicates, which are canon names.

--check validates and compares the rendered files with the ones on disk; it never
writes. Exit 1 on a validation error or a stale file. Prints the counts every run.
Standard library only; all text goes through textio (exactly one BOM).
"""
import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textio  # noqa: E402

LIST_FILE = "cybernetics_seller_names.txt"
REGISTER = os.path.join(HERE, "eotg_lint_register.json")
OUT_CUSTOM = "common/customizable_localization/eotg_aug_seller_names.txt"
OUT_ROLLS = "common/scripted_effects/eotg_aug_seller_roll_effects.txt"
OUT_LOC = "localization/english/eotg_aug_seller_names_l_english.yml"

SECTIONS = ("companies", "gangs", "syndicates")
MIN_COUNT = {"companies": 2, "gangs": 1, "syndicates": 1}
MAX_LEN = 32
ID_MAX = 40
# The Patron's syndicate is named (owner ruling, 2026-10-05). False drops the
# syndicate custom-loc keys and roll effects again.
PATRON_NAMED = True

FLAG = {"companies": "eotg_aug_co_", "gangs": "eotg_aug_gang_", "syndicates": "eotg_aug_syn_"}
LOCKEY = {"companies": "eotg_aug_seller_co_", "gangs": "eotg_aug_seller_gang_",
          "syndicates": "eotg_aug_seller_syn_"}

# Fallback keys and their fixed text (spec §7.3)
FALLBACK = [
    ("eotg_aug_seller_fallback_company", "a sanctioned clinic"),
    ("eotg_aug_seller_fallback_gang", "back-street operators"),
    ("eotg_aug_seller_fallback_vendor_careful", "the careful vendor"),
    ("eotg_aug_seller_fallback_vendor_bold", "the bold vendor"),
    ("eotg_aug_seller_fallback_clinic_of_record", "a sanctioned clinic"),
    ("eotg_aug_seller_fallback_syndicate", "the syndicate"),
    ("eotg_aug_seller_fallback_rival_syndicate", "a rival syndicate"),
]

# Custom loc key -> (list, how the text's trigger reads the flag, fallback key)
CUSTOM = [
    ("eotg_aug_cl_company", "companies", "var:eotg_aug_seller_company", "eotg_aug_seller_fallback_company"),
    ("eotg_aug_cl_gang", "gangs", "var:eotg_aug_seller_gang", "eotg_aug_seller_fallback_gang"),
    ("eotg_aug_cl_vendor_careful", "companies", "var:eotg_aug_vendor_careful",
     "eotg_aug_seller_fallback_vendor_careful"),
    ("eotg_aug_cl_vendor_bold", "companies", "var:eotg_aug_vendor_bold", "eotg_aug_seller_fallback_vendor_bold"),
    ("eotg_aug_cl_clinic_of_record", "companies", "var:eotg_aug_clinic_of_record",
     "eotg_aug_seller_fallback_clinic_of_record"),
    ("eotg_aug_cl_syndicate_offer", "syndicates", "var:eotg_patron_syndicate_passthrough",
     "eotg_aug_seller_fallback_syndicate"),
    ("eotg_aug_cl_syndicate", "syndicates", "STORY", "eotg_aug_seller_fallback_syndicate"),
    ("eotg_aug_cl_rival_syndicate", "syndicates", "var:eotg_aug_rival_syndicate",
     "eotg_aug_seller_fallback_rival_syndicate"),
]

# Roll effect -> (list, with an EXCLUDE parameter)
ROLLS = [
    ("eotg_aug_roll_company_effect", "companies", False),
    ("eotg_aug_roll_company_except_effect", "companies", True),
    ("eotg_aug_roll_gang_effect", "gangs", False),
    ("eotg_aug_roll_syndicate_effect", "syndicates", False),
    ("eotg_aug_roll_syndicate_except_effect", "syndicates", True),
]

ALLOWED_PUNCT = set(" &'.-")
GENERATED = ("# GENERATED. Edit `cybernetics_seller_names.txt` and run "
             "`python docs/tools/gen_seller_names.py`.")


class NameError_(Exception):
    pass


def derive_id(name, section):
    s = name.strip()
    if section == "syndicates" and s.lower().startswith("the "):
        s = s[4:]
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:ID_MAX].strip("_")


def parse(text, path):
    """-> ({section: [(name, line)]}, [errors])"""
    lists = {s: [] for s in SECTIONS}
    errors = []
    cur = None
    for n, raw in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^\[(.*)\]$", line)
        if m:
            if m.group(1) not in SECTIONS:
                errors.append("%s:%d: unknown header [%s] (only [companies], [gangs], [syndicates])"
                              % (path, n, m.group(1)))
                cur = None
            else:
                cur = m.group(1)
            continue
        if cur is None:
            errors.append("%s:%d: '%s' is not under [companies], [gangs] or [syndicates]" % (path, n, line))
            continue
        lists[cur].append((line, n))
    return lists, errors


def load_rules(path=REGISTER):
    d = json.loads(textio.read_text(path)[0])

    def comp(items):
        return [(t["term"], re.compile(t["regex"], 0 if t.get("case") else re.I)) for t in items]
    banned = d.get("name_banned_words", {})
    return {
        "error": comp(d.get("error", [])),
        "name_never": comp(d.get("name_never", [])),
        "all": comp(banned.get("all", [])),
        "companies": comp(banned.get("companies", [])),
        "gangs": comp(banned.get("gangs", [])),
        "syndicate_never": comp(d.get("syndicate_never", [])),
        "syndicate_warn": comp(d.get("syndicate_warn", [])),
    }


def _chars_ok(name):
    for ch in name:
        if ch in ALLOWED_PUNCT or ch.isdigit():
            continue
        if unicodedata.category(ch).startswith("L"):
            continue
        return ch
    return None


def validate(lists, rules, path):
    """-> (errors, warnings)"""
    errors, warnings = [], []
    seen_names = {}   # lower name -> (section, line)
    for sec in SECTIONS:
        ids = {}
        for name, n in lists[sec]:
            where = "%s:%d" % (path, n)
            if len(name) > MAX_LEN:
                errors.append("%s: '%s' is %d characters; the limit is %d" % (where, name, len(name), MAX_LEN))
            bad = _chars_ok(name)
            if bad is not None:
                errors.append("%s: '%s' has a character that is not allowed: %r "
                              "(letters, digits, spaces and & ' . - only)" % (where, name, bad))
            low = name.lower()
            if low in seen_names:
                psec, pn = seen_names[low]
                errors.append("%s: '%s' is a duplicate of line %d (in [%s])" % (where, name, pn, psec))
            else:
                seen_names[low] = (sec, n)
            i = derive_id(name, sec)
            if not i:
                errors.append("%s: '%s' gives an empty id; use letters or digits" % (where, name))
            elif i in ids:
                errors.append("%s: '%s' gives the id '%s', the same as line %d; rename one"
                              % (where, name, i, ids[i]))
            else:
                ids[i] = n
            if sec == "gangs" and low.startswith("the "):
                errors.append("%s: '%s': drop 'the'; the game adds it" % (where, name))
            if sec == "syndicates":
                for term, rx in rules["syndicate_never"]:
                    if rx.search(name):
                        errors.append("%s: '%s' is not allowed as a syndicate (%s)" % (where, name, term))
                for term, rx in rules["syndicate_warn"]:
                    if rx.search(name):
                        warnings.append("%s: '%s' (%s): allowed, but check it with the lore-keeper; "
                                        "your call" % (where, name, term))
                continue
            for group, label in (("error", "never-name"), ("name_never", "never-name"),
                                 ("all", "banned word"), (sec, "banned word for [%s]" % sec)):
                for term, rx in rules[group]:
                    if rx.search(name):
                        errors.append("%s: '%s' uses a %s: %s" % (where, name, label, term))
    for sec in SECTIONS:
        if len(lists[sec]) < MIN_COUNT[sec]:
            errors.append("%s: [%s] needs at least %d name%s (it has %d)"
                          % (path, sec, MIN_COUNT[sec], "" if MIN_COUNT[sec] == 1 else "s", len(lists[sec])))
    return errors, warnings


def _entries(lists, sec):
    return [(name, derive_id(name, sec)) for name, _ in lists[sec]]


def counts_line(lists):
    return "companies: %d  gangs: %d  syndicates: %d" % tuple(len(lists[s]) for s in SECTIONS)


def render_custom(lists):
    out = [GENERATED,
           "# Seller names for cybernetics events (docs/specs/cybernetics_v2_seller_names.md).",
           "# Each key reads a character variable holding a flag, set once by a roll effect",
           "# (vanilla GetAnimalTypeCaptive, common/customizable_localization/",
           "# 04_ep2_hunt_custom_loc.txt:413-418). No random_valid: the text never re-rolls.",
           "# " + counts_line(lists), ""]
    for key, sec, reads, fb in CUSTOM:
        if sec == "syndicates" and not PATRON_NAMED:
            continue
        out += ["%s = {" % key, "    type = character", ""]
        for name, i in _entries(lists, sec):
            flag = "flag:%s%s" % (FLAG[sec], i)
            if reads == "STORY":
                trig = ("any_owned_story = { story_type = eotg_story_aug_patron  "
                        "var:eotg_syndicate ?= %s }" % flag)
            else:
                trig = "%s ?= %s" % (reads, flag)
            out += ["    text = {",
                    "        trigger = { %s }" % trig,
                    "        localization_key = %s%s" % (LOCKEY[sec], i),
                    "    }"]
        out += ["    text = {",
                "        localization_key = %s" % fb,
                "        fallback = yes",
                "    }",
                "}", ""]
    return "\n".join(out)


def render_rolls(lists):
    out = [GENERATED,
           "# Roll a seller into a character variable holding a flag (param VAR); the",
           "# _except variants skip the flag held in var:$EXCLUDE$. Shape: vanilla random_list",
           "# entries with a trigger, events/story_cycles/story_cycle_pet_animal_events.txt:108-200.",
           "# Callers roll in an event's immediate, inside hidden_effect.",
           "# " + counts_line(lists), ""]
    for key, sec, exclude in ROLLS:
        if sec == "syndicates" and not PATRON_NAMED:
            continue
        entries = list(_entries(lists, sec))
        flags = ["flag:%s%s" % (FLAG[sec], i) for _name, i in entries]
        out.append("%s = {" % key)
        pad = "    "
        if exclude:
            # S3-2: never hand random_list a list whose every entry is excluded
            # (a single-entry list whose only name is var:$EXCLUDE$). Unrolled,
            # the variable stays unset and the custom loc falls back.
            out += ["    if = {", "        limit = {", "            OR = {"]
            out += ["                NOT = { var:$EXCLUDE$ ?= %s }" % f for f in flags]
            out += ["            }", "        }"]
            pad = "        "
        out.append(pad + "random_list = {")
        for flag in flags:
            out.append(pad + "    1 = {")
            if exclude:
                out.append(pad + "        trigger = { NOT = { var:$EXCLUDE$ ?= %s } }" % flag)
            out.append(pad + "        set_variable = { name = $VAR$  value = %s }" % flag)
            out.append(pad + "    }")
        out.append(pad + "}")
        if exclude:
            out.append("    }")
        out += ["}", ""]
    return "\n".join(out)


def _loc_escape(s):
    return s.replace('"', '\\"')


def render_loc(lists):
    out = ["l_english:",
           " " + GENERATED,
           " # " + counts_line(lists)]
    for sec in SECTIONS:
        for name, i in _entries(lists, sec):
            value = ("the " + name) if sec == "gangs" else name
            out.append(' %s%s:0 "%s"' % (LOCKEY[sec], i, _loc_escape(value)))
    for key, text in FALLBACK:
        out.append(' %s:0 "%s"' % (key, text))
    return "\n".join(out) + "\n"


def render_all(lists):
    return {OUT_CUSTOM: render_custom(lists), OUT_ROLLS: render_rolls(lists), OUT_LOC: render_loc(lists)}


def same_content(have, want):
    """True if the bytes on disk match the rendered bytes, ignoring line endings.

    A checkout with core.autocrlf=true has CRLF files on disk while the renderer writes
    LF, so a byte comparison would call every generated file stale."""
    if have is None:
        return False
    return have.replace(b"\r\n", b"\n") == want.replace(b"\r\n", b"\n")


def run(root, check=False, register=REGISTER, out=sys.stdout):
    path = os.path.join(root, LIST_FILE)
    if not os.path.exists(path):
        print("no %s in %s" % (LIST_FILE, root), file=out)
        return 1
    text, _ = textio.read_text(path)
    lists, errors = parse(text, LIST_FILE)
    verrs, warns = validate(lists, load_rules(register), LIST_FILE)
    errors += verrs
    for w in warns:
        print("warning: " + w, file=out)
    if errors:
        for e in errors:
            print("error: " + e, file=out)
        print("%d error(s); nothing written" % len(errors), file=out)
        return 1
    files = render_all(lists)
    if check:
        stale = []
        for rel, body in files.items():
            p = os.path.join(root, *rel.split("/"))
            want = textio.encode(body, bom=True)
            have = None
            if os.path.exists(p):
                with open(p, "rb") as fh:
                    have = fh.read()
            if not same_content(have, want):
                stale.append(rel)
        print(counts_line(lists), file=out)
        if stale:
            for rel in stale:
                print("STALE: " + rel, file=out)
            print("run: python docs/tools/gen_seller_names.py", file=out)
            return 1
        print("seller names are current", file=out)
        return 0
    print(counts_line(lists), file=out)
    for rel, body in files.items():
        p = os.path.join(root, *rel.split("/"))
        have = None
        if os.path.exists(p):
            with open(p, "rb") as fh:
                have = fh.read()
        if same_content(have, textio.encode(body, bom=True)):
            print("  unchanged " + rel, file=out)      # leave files others may be editing alone
            continue
        textio.write_text(p, body, bom=True, makedirs=True)
        print("  wrote " + rel, file=out)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(HERE)))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    return run(os.path.abspath(a.root), a.check)


if __name__ == "__main__":
    sys.exit(main())
