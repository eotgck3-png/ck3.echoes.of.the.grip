#!/usr/bin/env python3
"""TEST ONLY: generator for the "EotG Test: British Isles" sub-mod.

Never shipped. Reads vanilla CK3 (1.20) and writes this sub-mod's history,
bookmark, trigger override and generated loc, so the whole world can be rebuilt
after a CK3 update or after the owner edits the CSV files next to the README.

What the generated world is (M1, owner decision 2026-10-08):
  * ZONE (the editable line ZONE_EMPIRES below): de jure e_britannia, e_france,
    e_spain.
      - The Isles (ISLES_EMPIRE): vanilla 1066 holders, with the government mix
        and Unclaimed counties from isles_assignments.csv.
      - France and Spain: every county an independent Unsworn county (one
        pre-generated placeholder each, eotg_unclaimed_folk, the county's 1066
        culture and rite), except the "pocket" realms listed in the CSV.
  * OUTSIDE THE ZONE: the map and titles stay vanilla (nothing removed, so the
    ~600 vanilla files that name titles stay valid), but every county is held by
    one inert "offmap" holder per out-of-zone empire (eotg_test_offmap_government),
    non-capital baronies get no holding (so the engine generates no barons), and
    every living history character out there is retired (dies the day before
    the start), so no courts or rulers load.

Usage (from the repo root):
    python docs/test_submods/british_isles/tools/gen_history.py [--game <game dir>]

The script only ever writes inside docs/test_submods/british_isles/ and deletes
only its own generated output there first.
"""
import argparse
import collections
import csv
import hashlib
import io
import os
import re
import shutil
import sys

# ---------------------------------------------------------------- settings --
# The zone. One editable line: add e.g. 'e_germany' to bring it in.
ZONE_EMPIRES = ['e_britannia', 'e_france', 'e_spain']
# The empire whose titles keep their vanilla 1066 holders (the test zone).
ISLES_EMPIRE = 'e_britannia'
START = (1066, 9, 15)          # the 1066 bookmark date (vanilla bm_group_1066)
RETIRE_DATE = (1066, 9, 14)    # out-of-zone characters die the day before
MOVED_DATE = (1066, 9, 13)     # vanilla title blocks ON the start date move here (holders still alive)
OFFMAP_GOVERNMENT = 'eotg_test_offmap_government'
UNSWORN_GOVERNMENT = 'eotg_unclaimed_government'   # main mod
UNSWORN_TRAIT = 'eotg_unclaimed_folk'               # main mod
# History struggles/situations outside the zone that are not started. Vanilla
# starts each of them only behind a DLC check, so every script that reads them
# already copes with their absence.
NEUTRALISED_HISTORY = [
    'history/struggles/tgp_dynastic_cycle_history.txt',
    'history/struggles/tgp_silk_road_history.txt',
    'history/situations/mpo_the_great_steppe_history.txt',
]
# Governments whose ruler's capital barony must be their primary holding.
CAPITAL_HOLDING = {
    'tribal_government': 'tribal_holding',
    'republic_government': 'city_holding',
    'ecclesiastical_government': 'church_holding',
    'theocracy_government': 'church_holding',
}
DEFAULT_GAME = 'D:/SteamLibrary/steamapps/common/Crusader Kings III/game'

HERE = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(SUB, '..', '..', '..'))
GENERATED_DIRS = ['history', 'common/bookmarks']
GENERATED_FILES = [
    'common/scripted_triggers/eotg_vanilla_overrides_triggers.txt',
    'localization/english/eotg_test_bi_generated_l_english.yml',
]

# ------------------------------------------------------------------ parsing --
TOK = re.compile(r'"[^"]*"|#[^\n]*|[{}]|[<>!?]?=|[<>]|[^\s{}=<>!?#"]+')
DATE = re.compile(r'^\d+(\.\d+){0,2}$')   # vanilla also writes bare years ("1120 = {")


def tokens(text):
    for m in TOK.finditer(text):
        t = m.group(0)
        if t[0] == '#':
            continue
        yield t, m.start()


def parse(text):
    """Nested list of (key, value) pairs; a block value is a list."""
    toks = list(tokens(text))
    pos = 0

    def block():
        nonlocal pos
        out = []
        while pos < len(toks):
            t = toks[pos][0]
            if t == '}':
                pos += 1
                return out
            if pos + 1 < len(toks) and toks[pos + 1][0] in ('=', '?=', '<', '>', '<=', '>=', '!='):
                pos += 2
                if pos >= len(toks):
                    break
                v = toks[pos][0]
                pos += 1
                if v == '{':
                    out.append((t, block()))
                else:
                    out.append((t, v.strip('"')))
            elif t == '{':
                pos += 1
                out.append((None, block()))
            else:
                pos += 1
                out.append((t, None))
        return out
    return block()


def top_entries(text):
    """Top-level `key = { ... }` entries: (key, start of the key, index of the closing brace)."""
    out = []
    depth = 0
    pending = None
    prev = []
    for t, p in tokens(text):
        if t == '{':
            if depth == 0 and len(prev) >= 2 and prev[-1][0] == '=':
                pending = prev[-2]
            depth += 1
        elif t == '}':
            depth -= 1
            if depth == 0 and pending is not None:
                out.append((pending[0].strip('"'), pending[1], p))
                pending = None
            if depth < 0:
                raise ValueError('unbalanced braces')
        prev = (prev + [(t, p)])[-2:]
    if depth != 0:
        raise ValueError('unbalanced braces (depth %d at end)' % depth)
    return out


def dated_subblocks(text, start, close):
    """Dated `date = { ... }` blocks directly inside the entry text[start:close+1]:
    (date, start index, end index exclusive)."""
    out = []
    depth = 0
    prev = []
    open_at = None
    for t, p in tokens(text[start:close + 1]):
        if t == '{':
            depth += 1
            if depth == 2 and len(prev) >= 2 and prev[-1][0] == '=' and DATE.match(prev[-2][0]):
                open_at = (d(prev[-2][0]), start + prev[-2][1])
        elif t == '}':
            if depth == 2 and open_at is not None:
                out.append((open_at[0], open_at[1], start + p + 1))
                open_at = None
            depth -= 1
        prev = (prev + [(t, p)])[-2:]
    return out


def d(s):
    a = [int(x) for x in s.strip('"').split('.')]
    return tuple(a + [1] * (3 - len(a)))


def ds(t):
    return '%d.%d.%d' % t


def read(path):
    """Vanilla text, byte-exact round trip (latin-1), BOM kept separately."""
    raw = open(path, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    if bom:
        raw = raw[3:]
    return raw.decode('latin-1'), bom


def write_vanilla_copy(path, text, bom):
    """Write an override of a vanilla file with vanilla's own encoding."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        if bom:
            f.write(b'\xef\xbb\xbf')
        f.write(text.encode('latin-1'))


def write_new(path, text, bom=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        if bom:
            f.write(b'\xef\xbb\xbf')
        f.write(text.encode('utf-8'))


def blocks_upto(entry, limit):
    """Dated blocks of an entry, sorted, up to and including `limit`."""
    out = [(d(k), v) for k, v in entry if k and DATE.match(k) and isinstance(v, list)]
    out.sort(key=lambda x: x[0])
    return [(dt, v) for dt, v in out if dt <= limit]


def walk_files(root, rel):
    base = os.path.join(root, rel)
    for dirpath, _, files in os.walk(base):
        for f in sorted(files):
            if f.endswith('.txt'):
                full = os.path.join(dirpath, f)
                yield full, os.path.relpath(full, root).replace(os.sep, '/')


# ------------------------------------------------------------------- vanilla --
class Vanilla:
    def __init__(self, game):
        self.g = game
        self.load_titles()
        self.load_title_history()
        self.load_characters()
        self.load_provinces()
        self.load_faith_heads()
        self.load_name_lists()
        self.load_governments()

    def load_titles(self):
        self.titles = {}
        order = []

        def walk(items, parent):
            for k, v in items:
                if k and isinstance(v, list) and re.match(r'^[hekdcb]_', k):
                    t = {'parent': parent, 'province': None, 'landless': False, 'children': []}
                    for k2, v2 in v:
                        if k2 == 'province':
                            t['province'] = int(v2)
                        elif k2 == 'landless' and v2 == 'yes':
                            t['landless'] = True
                    self.titles[k] = t
                    order.append(k)
                    if parent:
                        self.titles[parent]['children'].append(k)
                    walk(v, k)
        for full, _ in walk_files(self.g, 'common/landed_titles'):
            walk(parse(read(full)[0]), None)
        # county -> baronies in file order; the first is the capital barony
        self.baronies = {k: [c for c in t['children'] if c.startswith('b_') and self.titles[c]['province']]
                         for k, t in self.titles.items() if k.startswith('c_')}
        self.counties = [k for k in order if k.startswith('c_') and self.baronies.get(k)]

    def ancestors(self, k):
        out = []
        while k:
            out.append(k)
            k = self.titles.get(k, {}).get('parent')
        return out

    def load_title_history(self):
        self.title_files = {}   # rel path -> (text, bom, [(key, close_idx)])
        self.state = {}         # title -> holder/liege/government at START
        for full, rel in walk_files(self.g, 'history/titles'):
            text, bom = read(full)
            entries = top_entries(text)
            self.title_files[rel] = (text, bom, entries)
            for k, v in parse(text):
                if not isinstance(v, list) or not k:
                    continue
                s = self.state.setdefault(k, {'holder': '0', 'liege': '0', 'government': None, 'file': rel})
                s['file'] = rel
                for _, b in blocks_upto(v, START):
                    for k3, v3 in b:
                        if k3 in ('holder', 'liege', 'government') and isinstance(v3, str):
                            s[k3] = v3

    def load_characters(self):
        self.char_files = {}    # rel -> (text, bom, entries)
        self.chars = {}
        for full, rel in walk_files(self.g, 'history/characters'):
            text, bom = read(full)
            self.char_files[rel] = (text, bom, top_entries(text))
            for k, v in parse(text):
                if not isinstance(v, list) or not k:
                    continue
                c = {'file': rel, 'birth': None, 'death': None, 'father': None, 'mother': None,
                     'spouses': set(), 'culture': None, 'rite': None, 'female': False,
                     'dynasty': None, 'dynasty_house': None, 'name': None, 'employer': None}
                for k2, v2 in v:
                    if k2 in ('father', 'mother', 'culture', 'rite', 'dynasty', 'dynasty_house', 'name') and isinstance(v2, str):
                        c[k2] = v2
                    elif k2 == 'female' and v2 == 'yes':
                        c['female'] = True
                    elif k2 == 'death':
                        c['death'] = (1, 1, 1)
                for dt, b in blocks_upto(v, (9999, 1, 1)):
                    for k3, v3 in b:
                        if k3 == 'birth' and c['birth'] is None:
                            c['birth'] = dt
                        elif k3 == 'death' and c['death'] is None:
                            c['death'] = dt
                        elif dt <= START and k3 in ('add_spouse', 'add_matrilineal_spouse') and isinstance(v3, str):
                            c['spouses'].add(v3)
                        elif dt <= START and k3 == 'remove_spouse' and isinstance(v3, str):
                            c['spouses'].discard(v3)
                        elif dt <= START and k3 in ('culture', 'rite', 'employer') and isinstance(v3, str):
                            c[k3] = v3
                self.chars[k] = c
        for k, c in self.chars.items():
            for s in list(c['spouses']):
                if s in self.chars:
                    self.chars[s]['spouses'].add(k)

    def alive(self, cid):
        c = self.chars.get(cid)
        return bool(c and c['birth'] and c['birth'] <= START and not (c['death'] and c['death'] <= START))

    def load_provinces(self):
        self.prov_files = {}
        self.prov = {}
        for full, rel in walk_files(self.g, 'history/provinces'):
            text, bom = read(full)
            self.prov_files[rel] = (text, bom, top_entries(text))
            for k, v in parse(text):
                if not (k and k.isdigit() and isinstance(v, list)):
                    continue
                p = {'file': rel, 'culture': None, 'rite': None, 'holding': None, 'special': False}
                for k2, v2 in v:
                    if k2 in ('culture', 'rite', 'holding') and isinstance(v2, str):
                        p[k2] = v2
                    elif k2 == 'special_building':
                        p['special'] = True
                for _, b in blocks_upto(v, START):
                    for k3, v3 in b:
                        if k3 in ('culture', 'rite', 'holding') and isinstance(v3, str):
                            p[k3] = v3
                        elif k3 == 'special_building':
                            p['special'] = True
                self.prov[int(k)] = p

    def load_faith_heads(self):
        self.faith_heads = set()
        pat = re.compile(r'\b(?:religious_head|head_of_rite)\s*=\s*([a-z_0-9]+)')
        for full, _ in walk_files(self.g, 'common/religion'):
            for m in pat.finditer(re.sub(r'#[^\n]*', '', read(full)[0])):
                if m.group(1) in self.titles:
                    self.faith_heads.add(m.group(1))

    def load_name_lists(self):
        culture_list = {}
        for full, _ in walk_files(self.g, 'common/culture/cultures'):
            for k, v in parse(read(full)[0]):
                if isinstance(v, list):
                    for k2, v2 in v:
                        if k2 == 'name_list' and isinstance(v2, str):
                            culture_list.setdefault(k, v2)
        lists = {}

        def flat(items):
            out = []
            for k, v in items:
                if isinstance(v, list):
                    out += flat(v)
                elif v is None and k:
                    out.append(k)
            return out
        for full, _ in walk_files(self.g, 'common/culture/name_lists'):
            # Name lists are UTF-8: decode them as such, the names are written to new files
            raw = open(full, 'rb').read().decode('utf-8-sig', errors='replace')
            for k, v in parse(raw):
                if isinstance(v, list):
                    entry = {}
                    for k2, v2 in v:
                        if k2 in ('male_names', 'female_names') and isinstance(v2, list):
                            entry[k2] = [n for n in flat(v2) if re.match(r'^[A-Za-z_][A-Za-z_0-9]*$', n)]
                    lists[k] = entry
        self.culture_names = {c: lists.get(nl, {}) for c, nl in culture_list.items()}

    def load_governments(self):
        self.governments = set()
        for full, _ in walk_files(self.g, 'common/governments'):
            for k, v in parse(read(full)[0]):
                if k and isinstance(v, list):
                    self.governments.add(k)


# ------------------------------------------------------------------- the CSV --
def read_csv(path):
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        lines = [l for l in f if l.strip() and not l.lstrip().startswith('#')]
    for r in csv.DictReader(lines):
        rows.append({k.strip(): (v or '').strip() for k, v in r.items() if k})
    return rows


def pick(seq, key):
    if not seq:
        return None
    h = int(hashlib.sha1(key.encode()).hexdigest(), 16)
    return seq[h % len(seq)]


# ----------------------------------------------------------------- generator --
class Build:
    def __init__(self, v, assignments, bookmark_rows):
        self.v = v
        self.errors = []
        self.notes = []
        self.final = {}        # title -> {'holder','liege','government'} explicit at START
        self.new_chars = {}    # id -> dict for generated characters
        self.gov_of = {}       # character -> government set by this build
        self.assignments = assignments
        self.bookmark_rows = bookmark_rows

    # zone helpers
    def zone_of(self, k):
        anc = self.v.ancestors(k)
        if ISLES_EMPIRE in anc:
            return 'isles'
        if any(e in anc for e in ZONE_EMPIRES):
            return 'mainland'
        return 'offmap'

    def root_of(self, k):
        return self.v.ancestors(k)[-1]

    def vanilla_holder(self, k):
        return self.v.state.get(k, {}).get('holder', '0').strip('"')

    def vanilla_liege(self, k):
        return self.v.state.get(k, {}).get('liege', '0').strip('"')

    def capital_province(self, county):
        return self.v.titles[self.v.baronies[county][0]]['province']

    # ------------------------------------------------------------ placeholders
    def unsworn(self, county):
        cid = 'eotg_test_bi_unsworn_' + county[2:]
        if cid not in self.new_chars:
            p = self.v.prov.get(self.capital_province(county), {})
            culture, rite = p.get('culture'), p.get('rite')
            if not culture or not rite:
                self.errors.append('%s: capital province %s has no 1066 culture/rite' % (county, self.capital_province(county)))
            female = int(hashlib.sha1(county.encode()).hexdigest(), 16) % 2 == 1
            names = self.v.culture_names.get(culture, {}).get('female_names' if female else 'male_names', [])
            age = 25 + int(hashlib.sha1(('age' + county).encode()).hexdigest(), 16) % 26
            self.new_chars[cid] = {
                'kind': 'unsworn', 'county': county, 'culture': culture, 'rite': rite, 'female': female,
                'name': pick(names, county) or 'Unsworn', 'birth': (START[0] - age, 1, 1)}
        return cid

    def offmap_holder(self, root, counties):
        cid = 'eotg_test_bi_offmap_' + root
        if cid not in self.new_chars:
            cul = collections.Counter()
            rit = collections.Counter()
            for c in counties:
                p = self.v.prov.get(self.capital_province(c), {})
                if p.get('culture'):
                    cul[p['culture']] += 1
                if p.get('rite'):
                    rit[p['rite']] += 1
            self.new_chars[cid] = {
                'kind': 'offmap', 'root': root, 'culture': cul.most_common(1)[0][0], 'rite': rit.most_common(1)[0][0],
                'female': False, 'name': 'eotg_test_bi_offmap_name', 'birth': (START[0] - 40, 1, 1), 'counties': len(counties)}
        return cid

    # ------------------------------------------------------------- assignment
    def assign(self):
        v = self.v
        # 1. defaults
        offmap_groups = collections.defaultdict(list)
        for c in v.counties:
            if self.zone_of(c) == 'offmap':
                offmap_groups[self.root_of(c)].append(c)
        for root, counties in offmap_groups.items():
            h = self.offmap_holder(root, counties)
            for c in counties:
                self.final[c] = {'holder': h, 'liege': '0', 'government': OFFMAP_GOVERNMENT}
        for c in v.counties:
            if self.zone_of(c) == 'mainland':
                self.final[c] = {'holder': self.unsworn(c), 'liege': '0', 'government': UNSWORN_GOVERNMENT}
        # every other title with a 1066 holder: vacated, except the Isles,
        # faith-head titles and counties (done above)
        self.isles_cultures = set()
        for c in v.counties:
            if self.zone_of(c) == 'isles':
                p = v.prov.get(self.capital_province(c), {})
                if p.get('culture'):
                    self.isles_cultures.add(p['culture'])
        every = set(v.state) | set(v.titles)
        for k in every:
            if k in self.final or k.startswith('b_'):
                continue
            if k in v.titles and self.zone_of(k) == 'isles':
                continue
            if k in v.faith_heads:
                continue
            if k not in v.titles or v.titles[k]['landless']:
                # titles made by history effects (landless adventurers): an Isles
                # adventurer keeps his (e.g. Hereward the Wake)
                h = self.vanilla_holder(k)
                if v.alive(h) and v.chars[h]['culture'] in self.isles_cultures:
                    self.notes.append('%s: kept by %s (%s), an Isles landless title' % (k, h, v.chars[h]['name']))
                    continue
            if self.vanilla_holder(k) != '0':
                self.final[k] = {'holder': '0', 'liege': None, 'government': None}

        # 2. the CSV
        scoped = []
        for r in self.assignments:
            t = r['title']
            if t not in v.titles:
                self.errors.append('CSV: unknown title %s' % t)
                continue
            if self.zone_of(t) == 'offmap':
                self.errors.append('CSV: %s is outside the zone %s' % (t, ZONE_EMPIRES))
                continue
            holder = r.get('holder', 'vanilla') or 'vanilla'
            liege = r.get('liege', '')
            gov = r.get('government', '')
            entry = {'holder': None, 'liege': None, 'government': None}
            if holder == 'vanilla':
                h = self.vanilla_holder(t)
                if h != '0' and not v.alive(h):
                    self.errors.append('CSV: %s vanilla holder %s is not alive at the start' % (t, h))
                    continue
                entry['holder'] = h
            elif holder == 'unsworn':
                if not t.startswith('c_'):
                    self.errors.append('CSV: unsworn is for counties only (%s)' % t)
                    continue
                entry = {'holder': self.unsworn(t), 'liege': '0', 'government': UNSWORN_GOVERNMENT}
            elif holder == 'none':
                entry = {'holder': '0', 'liege': None, 'government': None}
            else:
                if not v.alive(holder):
                    self.errors.append('CSV: %s holder %s is not a living vanilla character at %s' % (t, holder, ds(START)))
                    continue
                entry['holder'] = holder
            if liege and liege != 'vanilla':
                entry['liege'] = liege
            if gov:
                if gov not in v.governments:
                    self.errors.append('CSV: %s unknown government %s' % (t, gov))
                    continue
                scoped.append((t, gov, r.get('scope', 'holder') or 'holder'))
            self.final[t] = entry
        self.scoped = scoped

        # 3. baronies with their own holder in vanilla history: outside the Isles,
        # and inside Unclaimed Isles counties, they follow the county's new holder
        for b, t in v.titles.items():
            if not b.startswith('b_') or self.vanilla_holder(b) == '0':
                continue
            county = t['parent']
            ch = self.holder_of(county)
            if self.zone_of(b) == 'isles' and ch not in self.new_chars:
                continue
            self.final[b] = {'holder': ch, 'liege': None, 'government': None}

        # 4. placeholders made for a county the CSV then gave to someone else
        used = {e['holder'] for e in self.final.values()}
        for cid in [x for x in self.new_chars if x not in used]:
            del self.new_chars[cid]

    def holder_of(self, k):
        # Every title whose holder changes is in self.final (assign() vacates
        # everything outside the Isles and the faith-head titles), so anything
        # else keeps its vanilla 1066 holder.
        if k in self.final and self.final[k].get('holder') is not None:
            return self.final[k]['holder']
        return self.vanilla_holder(k)

    def liege_of(self, k):
        if k in self.final and self.final[k].get('liege') is not None:
            return self.final[k]['liege']
        return self.vanilla_liege(k)

    def resolve(self):
        v = self.v
        zone_titles = [k for k in v.titles if self.zone_of(k) != 'offmap' and not k.startswith('b_')]
        # lieges must point at a held title; otherwise the title is independent.
        # Every title with a holder, so kept faith-head titles (d_sunni -> k_persia, ...) too.
        for k in sorted(set(v.titles) | set(v.state) | set(self.final)):
            h = self.holder_of(k)
            l = self.liege_of(k)
            if h != '0' and l != '0' and self.holder_of(l) == '0':
                self.final.setdefault(k, {'holder': None, 'liege': None, 'government': None})['liege'] = '0'
                self.notes.append('%s: liege %s has no holder at the start, made independent' % (k, l))
        # liege graph between characters
        self.liege_char = {}
        self.held = collections.defaultdict(list)
        for k in zone_titles:
            h = self.holder_of(k)
            if h == '0':
                continue
            self.held[h].append(k)
        for h, ts in self.held.items():
            best = None
            for k in ts:
                l = self.liege_of(k)
                if l != '0':
                    lh = self.holder_of(l)
                    if lh not in ('0', h):
                        best = lh
            if best:
                self.liege_char[h] = best
        # governments from the CSV
        for t, gov, scope in self.scoped:
            targets = set()
            h = self.holder_of(t)
            if scope in ('holder', 'realm') and h != '0':
                targets.add(h)
            if scope == 'realm' and h != '0':
                for c in self.held:
                    x, seen = c, set()
                    while x in self.liege_char and x not in seen:
                        seen.add(x)
                        x = self.liege_char[x]
                        if x == h:
                            targets.add(c)
                            break
            if scope == 'dejure':
                for c in v.counties:
                    if t in v.ancestors(c):
                        ch = self.holder_of(c)
                        if ch != '0':
                            targets.add(ch)
            if not targets:
                self.errors.append('CSV: government %s on %s reaches nobody (scope %s)' % (gov, t, scope))
            for c in targets:
                if c in self.new_chars:
                    continue    # placeholders keep their own government
                self.gov_of[c] = gov
        # write one government line per character, on each title they hold in the zone
        for c, gov in self.gov_of.items():
            for k in self.held.get(c, []):
                e = self.final.setdefault(k, {'holder': None, 'liege': None, 'government': None})
                e['government'] = gov

    # ------------------------------------------------------- who stays alive
    def keep_set(self):
        v = self.v
        keep = set()
        for k in list(self.final) + list(v.titles):
            h = self.holder_of(k)
            if h not in ('0', None) and h in v.chars:
                keep.add(h)
        holders = set(keep)
        isles_cultures = self.isles_cultures
        children = collections.defaultdict(set)
        for cid, c in v.chars.items():
            for p in (c['father'], c['mother']):
                if p:
                    children[p].add(cid)
        for h in holders:
            c = v.chars[h]
            fam = set(c['spouses']) | children[h] | {c['father'], c['mother']}
            for p in (c['father'], c['mother']):
                if p:
                    fam |= children[p]
            keep |= {x for x in fam if x}
        for cid, c in v.chars.items():
            if c['culture'] in isles_cultures:
                keep.add(cid)
        self.keep = {x for x in keep if v.alive(x)}
        # A kept courtier whose employer is retired would sit in a dead court:
        # retire them too (holders and their close family always stay).
        family = set(holders)
        for h in holders:
            c = v.chars[h]
            family |= {x for x in (set(c['spouses']) | children[h] | {c['father'], c['mother']}) if x}
        changed = True
        while changed:
            changed = False
            for x in list(self.keep):
                e = v.chars[x].get('employer')
                if x not in family and e and e not in self.keep:
                    self.keep.discard(x)
                    changed = True
        self.retire = {cid for cid in v.chars if v.alive(cid) and cid not in self.keep
                       and v.chars[cid]['birth'] < RETIRE_DATE}
        # Kept family members whose employer is retired go to a living relative who
        # holds land (parents, spouses, siblings, children, in that order).
        self.employer_fix = {}
        for x in sorted(self.keep):
            e = v.chars[x].get('employer')
            if not e or e in self.keep:
                continue
            if x in holders:
                self.notes.append('%s (%s): a ruler whose vanilla employer %s is retired; left as is' % (x, v.chars[x]['name'], e))
                continue
            c = v.chars[x]
            sibs = set()
            for par in (c['father'], c['mother']):
                if par:
                    sibs |= children[par]
            order = [c['father'], c['mother']] + sorted(c['spouses']) + sorted(sibs - {x}) + sorted(children[x])
            new = next((r for r in order if r and r in holders and r in self.keep), None)
            if new:
                self.employer_fix[x] = new
                self.notes.append('%s (%s): employer %s is retired; moved to relative %s (%s)' % (
                    x, c['name'], e, new, v.chars[new]['name']))
            else:
                self.notes.append('%s (%s): employer %s is retired and no landed relative is kept' % (x, c['name'], e))
        for h in holders:
            if not v.alive(h):
                self.errors.append('holder %s is not alive at %s' % (h, ds(START)))

    # --------------------------------------------------------------- writers
    def block_for(self, k):
        e = self.final.get(k)
        if not e:
            return None
        lines = []
        if e.get('liege') is not None:
            lines.append('liege = %s' % e['liege'])
        if e.get('holder') is not None:
            lines.append('holder = %s' % e['holder'])
        if e.get('government'):
            lines.append('government = %s' % e['government'])
        if not lines:
            return None
        return lines

    def write_titles(self, out):
        v = self.v
        written = set()
        tag = '\t# EOTG TEST (british_isles, gen_history.py): the 1066 start\n'
        for rel, (text, bom, entries) in v.title_files.items():
            inserts = []
            last = {}
            for k, st, close in entries:
                last[k] = (st, close)
            for k, (st, close) in last.items():
                lines = self.block_for(k)
                if lines:
                    blk = tag + '\t%s = {\n%s\t}\n' % (ds(START), ''.join('\t\t%s\n' % l for l in lines))
                    inserts.append((close, close, blk))
                    written.add(k)
                    # A vanilla block on the start date itself is moved a day
                    # earlier, so ours is unambiguously the last word on that date.
                    for dt, a, _ in dated_subblocks(text, st, close):
                        if dt == START:
                            n = len(text[a:].split('=', 1)[0].rstrip())
                            inserts.append((a, a + n, ds(MOVED_DATE)))
                            self.notes.append('%s (%s): vanilla block on %s moved to %s' % (k, rel, ds(START), ds(MOVED_DATE)))
            for a, b2, blk in sorted(inserts, reverse=True):
                text = text[:a] + blk + text[b2:]
            write_vanilla_copy(os.path.join(out, rel), text, bom)
        rest =[k for k in self.final if k not in written and self.block_for(k)]
        body = ['# TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.',
                '# Titles that have no vanilla history file entry but need a holder at the start.', '']
        for k in sorted(rest, key=lambda x: (x[0], x)):
            body.append('%s = {' % k)
            body.append('\t%s = {' % ds(START))
            body += ['\t\t%s' % l for l in self.block_for(k)]
            body.append('\t}')
            body.append('}')
        write_new(os.path.join(out, 'history/titles/eotg_test_bi_titles.txt'), '\n'.join(body) + '\n', bom=True)
        self.count_new_title_entries = len(rest)

    def write_characters(self, out):
        v = self.v
        changed = collections.defaultdict(list)
        for cid in set(self.retire) | set(self.employer_fix):
            changed[v.chars[cid]['file']].append(cid)
        for rel, ids in changed.items():
            text, bom, entries = v.char_files[rel]
            ids = set(ids)
            last = {}
            for k, st, close in entries:
                if k in ids:
                    last[k] = (st, close)
            inserts = []
            for k, (st, close) in last.items():
                if k in self.employer_fix:
                    inserts.append((close, close, '\t%s = { employer = %s }\t# EOTG TEST (british_isles): vanilla employer retired\n'
                                    % (ds(START), self.employer_fix[k])))
                    continue
                b = v.chars[k]['birth']
                when = max(RETIRE_DATE, b)
                inserts.append((close, close, '\t%s = { death = yes }\t# EOTG TEST (british_isles): retired, outside the test zone\n' % ds(when)))
                # history after the death would act on a dead character: dropped
                for dt, a, e in dated_subblocks(text, st, close):
                    if dt > when:
                        inserts.append((a, e, ''))
            for a, b2, blk in sorted(inserts, reverse=True):
                text = text[:a] + blk + text[b2:]
            write_vanilla_copy(os.path.join(out, rel), text, bom)
        self.char_files_written = len(changed)
        # generated characters
        lines = ['# TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.',
                 '# Unsworn placeholders (one per Unclaimed county; main mod frontier_unclaimed_regions.md',
                 '# §5.1 option H, pre-split so no create_character runs at game start) and the offmap holders',
                 '# (one per empire outside the test zone).',
                 '# Bare culture/rite keys, as vanilla 1.20 history writes them (history/characters/*.txt).', '']
        for cid in sorted(self.new_chars):
            c = self.new_chars[cid]
            lines.append('%s = {' % cid)
            lines.append('\tname = "%s"' % c['name'])
            if c['female']:
                lines.append('\tfemale = yes')
            lines.append('\tculture = %s' % c['culture'])
            lines.append('\trite = %s' % c['rite'])
            if c['kind'] == 'unsworn':
                lines.append('\ttrait = %s\t# the government\'s can_get_government reads it' % UNSWORN_TRAIT)
                lines.append('\t# %s' % c['county'])
            else:
                lines.append('\tdisallow_random_traits = yes')
                lines.append('\t# offmap holder for %s (%d counties)' % (c['root'], c['counties']))
            lines.append('\t%s = {' % ds(c['birth']))
            lines.append('\t\tbirth = yes')
            lines.append('\t}')
            lines.append('}')
            lines.append('')
        write_new(os.path.join(out, 'history/characters/eotg_test_bi_characters.txt'), '\n'.join(lines), bom=True)

    def write_provinces(self, out):
        v = self.v
        changes = {}     # province -> holding
        for c in v.counties:
            h = self.holder_of(c)
            barons = v.baronies[c]
            kind = None
            if h in self.new_chars:
                kind = self.new_chars[h]['kind']
            gov = self.gov_of.get(h)
            if kind in ('offmap', 'unsworn'):
                for b in barons[1:]:
                    p = v.titles[b]['province']
                    pr = v.prov.get(p)
                    if pr and pr['holding'] not in (None, 'none') and not pr['special']:
                        changes[p] = 'none'
            if gov in CAPITAL_HOLDING:
                p = self.capital_province(c)
                pr = v.prov.get(p)
                want = CAPITAL_HOLDING[gov]
                if pr and pr['holding'] != want:
                    changes[p] = want
                    self.notes.append('%s: capital province %d holding %s -> %s (%s)' % (c, p, pr['holding'], want, gov))
        byfile = collections.defaultdict(dict)
        for p, hold in changes.items():
            byfile[v.prov[p]['file']][p] = hold
        for rel, ps in byfile.items():
            text, bom, entries = v.prov_files[rel]
            last = {}
            for k, _, close in entries:
                if k.isdigit() and int(k) in ps:
                    last[int(k)] = close
            inserts = [(close, '\t%s = { holding = %s }\t# EOTG TEST (british_isles)\n' % (ds(START), ps[p]))
                       for p, close in last.items()]
            for close, blk in sorted(inserts, reverse=True):
                text = text[:close] + blk + text[close:]
            write_vanilla_copy(os.path.join(out, rel), text, bom)
        self.prov_changes = changes
        self.prov_files_written = len(byfile)

    def write_wars(self, out):
        v = self.v
        removed = []
        for full, rel in walk_files(v.g, 'history/wars'):
            text, bom = read(full)
            spans = []
            depth = 0
            start = None
            toks = list(tokens(text))
            for i, (t, p) in enumerate(toks):
                if t == '{':
                    if depth == 0 and i >= 2 and toks[i - 1][0] == '=' and toks[i - 2][0] == 'war':
                        start = toks[i - 2][1]
                    depth += 1
                elif t == '}':
                    depth -= 1
                    if depth == 0 and start is not None:
                        spans.append((start, p + 1))
                        start = None
            drop = []
            for s, e in spans:
                w = dict((k, val) for k, val in parse(text[s:e])[0][1])
                sd, ed = d(w.get('start_date', '1.1.1')), d(w.get('end_date', '9999.1.1'))
                if sd <= START < ed:
                    drop.append((s, e))
                    removed.append(w.get('name', '?'))
            for s, e in sorted(drop, reverse=True):
                text = text[:s] + '# EOTG TEST (british_isles): war active at the start removed\n' + text[e:]
            if drop:
                write_vanilla_copy(os.path.join(out, rel), text, bom)
        self.wars_removed = removed

    def write_neutralised(self, out):
        for rel in NEUTRALISED_HISTORY:
            src = os.path.join(self.v.g, rel)
            if not os.path.exists(src):
                self.errors.append('neutralised file missing in vanilla: %s' % rel)
                continue
            write_new(os.path.join(out, rel),
                      '# TEST ONLY: EotG Test: British Isles (tools/gen_history.py).\n'
                      '# Overrides vanilla %s by name: this struggle/situation lies outside the test\n'
                      '# zone and is not started. Vanilla starts it only behind a DLC check, so every\n'
                      '# script that reads it already copes with its absence.\n' % rel, bom=True)

    def write_bookmarks(self, out):
        v = self.v
        bm_text = read(os.path.join(v.g, 'common/bookmarks/bookmarks/00_bookmarks.txt'))[0]
        name_of = {}
        for k, val in parse(bm_text):
            if isinstance(val, list):
                for k2, v2 in val:
                    if k2 == 'character' and isinstance(v2, list):
                        dd = dict((a, b) for a, b in v2 if isinstance(b, str))
                        if 'history_id' in dd and 'name' in dd:
                            name_of.setdefault(dd['history_id'], dd['name'])
        portraits = set(os.path.splitext(f)[0] for f in os.listdir(os.path.join(v.g, 'common/bookmark_portraits')))
        loc = []
        body = ['# TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.',
                '# Overrides vanilla 00_bookmarks.txt BY NAME: only the 1066 start is offered, because',
                '# this sub-mod replaces history/titles for 1066.9.15 only. The key bm_1066_hastings is',
                '# kept so vanilla\'s bookmark art and title loc still apply.', '',
                'bm_1066_hastings = {', '\tstart_date = %s' % ds(START), '\tis_playable = yes',
                '\tgroup = bm_group_1066', '', '\tweight = { value = 100 }', '']
        self.bookmark_listed = []
        self.bookmark_skipped = []
        for r in self.bookmark_rows:
            hid = r['history_id']
            c = v.chars.get(hid)
            if not c or not v.alive(hid) or hid not in self.keep:
                self.errors.append('bookmark: %s is not a living kept character' % hid)
                continue
            title = r['title']
            if self.holder_of(title) != hid:
                self.errors.append('bookmark: %s does not hold %s at the start' % (hid, title))
            name = name_of.get(hid) or ('eotg_test_bi_bm_%s' % hid)
            if name not in portraits:
                # Tiger: "bookmark portrait ... not found in common/bookmark_portraits ...
                # This causes a crash". Portraits are DNA files made in game; we cannot
                # author one, so the character is left off the screen (pick them on the map).
                self.bookmark_skipped.append((hid, r.get('label') or c['name'], title))
                continue
            if name.startswith('eotg_test_bi_bm_'):
                loc.append((name, r.get('label') or c['name'] or hid))
                loc.append((name + '_desc', r.get('desc') or ''))
            body.append('\t# %s (history id %s)%s' % (r.get('label', ''), hid, '' if name in portraits else
                                                    ' -- no vanilla bookmark portrait for this name'))
            body.append('\tcharacter = {')
            body.append('\t\tname = "%s"' % name)
            if c['dynasty']:
                body.append('\t\tdynasty = %s' % c['dynasty'])
            elif c['dynasty_house']:
                body.append('\t\tdynasty_house = %s' % c['dynasty_house'])
            body.append('\t\tdynasty_splendor_level = 1')
            body.append('\t\ttype = %s' % ('female' if c['female'] else 'male'))
            body.append('\t\thistory_id = %s' % hid)
            body.append('\t\tbirth = %s' % ds(c['birth']))
            body.append('\t\ttitle = %s' % title)
            body.append('\t\tgovernment = %s' % (r['government'] or 'feudal_government'))
            body.append('\t\tculture = %s' % c['culture'])
            body.append('\t\treligion = %s' % c['rite'])
            body.append('\t\tdifficulty = "BOOKMARK_CHARACTER_DIFFICULTY_%s"' % (r.get('difficulty') or 'MEDIUM').upper())
            body.append('\t\tposition = { %s %s }' % (r['x'], r['y']))
            body.append('\t\tanimation = personality_rational')
            body.append('\t}')
            body.append('')
            self.bookmark_listed.append((hid, name, title, r['government']))
        body.append('}')
        write_new(os.path.join(out, 'common/bookmarks/bookmarks/00_bookmarks.txt'), '\n'.join(body) + '\n', bom=True)
        write_new(os.path.join(out, 'common/bookmarks/groups/00_bookmark_groups.txt'),
                  '# TEST ONLY: EotG Test: British Isles (tools/gen_history.py). Overrides vanilla by name:\n'
                  '# only the 1066 group, which holds the one bookmark this sub-mod offers.\n'
                  'bm_group_1066 = {\n\tdefault_start_date = %s\n}\n' % ds(START), bom=True)
        self.bookmark_loc = loc

    def write_challenge(self, out):
        """Vanilla challenge characters, overridden BY NAME: only the 1066 ones whose
        character is alive and still holds their title in this sub-mod."""
        v = self.v
        rel = 'common/bookmarks/challenge_characters/00_challenge_characters.txt'
        text, bom = read(os.path.join(v.g, rel))
        parsed = dict((k, val) for k, val in parse(text) if k and isinstance(val, list))
        kept = []
        self.challenge_kept = []
        for k, st, close in top_entries(text):
            e = parsed.get(k)
            if not e:
                continue
            sd = dict((a, b) for a, b in e if isinstance(b, str)).get('start_date')
            ch = next((b for a, b in e if a == 'character' and isinstance(b, list)), None)
            if not sd or d(sd) != START or ch is None:
                continue
            cd = dict((a, b) for a, b in ch if isinstance(b, str))
            hid, title = cd.get('history_id'), cd.get('title')
            if hid in self.keep and title and self.holder_of(title) == hid:
                kept.append(text[st:close + 1])
                self.challenge_kept.append((k, hid, title))
        body = ('# TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.\n'
                '# Overrides vanilla %s BY NAME: only the 1066.9.15 challenge characters who are alive\n'
                '# and still hold their title in this sub-mod (the others are retired or landless here).\n\n' % rel)
        write_vanilla_copy(os.path.join(out, rel), body + '\n\n'.join(kept) + '\n', True)

    def write_trigger_override(self, out):
        """Pitfalls §16: copy programmatically, assert the anchors, diff against vanilla."""
        vpath = os.path.join(self.v.g, 'common/scripted_triggers/00_war_and_peace_triggers.txt')
        mpath = os.path.join(REPO, 'common/scripted_triggers/eotg_vanilla_overrides_triggers.txt')
        vtext = open(vpath, encoding='utf-8-sig').read()
        mtext = open(mpath, encoding='utf-8-sig').read()

        def block(text):
            lines = text.split('\n')
            i = [n for n, l in enumerate(lines) if l.startswith('herders_and_tributary_constraints = {')]
            assert len(i) == 1, 'herders_and_tributary_constraints: expected exactly one definition'
            depth = 0
            for n in range(i[0], len(lines)):
                depth += lines[n].count('{') - lines[n].count('}')
                if depth == 0:
                    return lines[i[0]:n + 1]
            raise AssertionError('unterminated block')
        van = block(vtext)
        main = block(mtext)
        eotg = [n for n, l in enumerate(main) if l.rstrip().endswith(('# EOTG (attacker)', '# EOTG (defender)'))]
        assert len(eotg) == 2, 'main mod override: expected exactly two "# EOTG" lines, found %d' % len(eotg)
        stripped = [l for n, l in enumerate(main) if n not in eotg]
        assert stripped == van, ('the main mod override is not vanilla + its two EOTG lines; '
                                 're-copy it there first (pitfalls §2/§16)')
        out_lines = []
        for n, l in enumerate(main):
            out_lines.append(l)
            if n in eotg:
                indent = re.match(r'\s*', l).group(0)
                if l.rstrip().endswith('(attacker)'):
                    out_lines.append(indent + 'NOT = { government_has_flag = eotg_test_government_is_offmap }   # EOTG TEST (offmap attacker)')
                else:
                    out_lines.append(indent + 'government_has_flag = eotg_test_government_is_offmap   # EOTG TEST (offmap defender)')
        added = [l for l in out_lines if l not in van]
        assert len(added) == 4 and [l for l in out_lines if l in van] == van, 'diff against vanilla is not exactly 4 lines'
        assert out_lines.count('{') == out_lines.count('}') or sum(l.count('{') - l.count('}') for l in out_lines) == 0
        header = (
            '# -- eotg_vanilla_overrides_triggers.txt (TEST SUB-MOD COPY) ----------------\n'
            '# TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.\n'
            '# Same file name as the main mod\'s override, so it REPLACES that file (later mod wins)\n'
            '# and the key is still defined exactly once. Body = vanilla\n'
            '# 00_war_and_peace_triggers.txt herders_and_tributary_constraints, plus the main mod\'s\n'
            '# two "# EOTG" lines (Unsworn), plus two "# EOTG TEST" lines (offmap holders).\n'
            '# The generator asserts that the diff from vanilla is exactly those four lines\n'
            '# (pitfalls §16). REGENERATE whenever the main mod\'s override or vanilla changes.\n'
            '# -----------------------------------------------------------------------------\n\n')
        write_new(os.path.join(out, 'common/scripted_triggers/eotg_vanilla_overrides_triggers.txt'),
                  header + '\n'.join(out_lines) + '\n', bom=True)
        self.trigger_added = added

    def write_loc(self, out):
        lines = ['l_english:',
                 ' # TEST ONLY: EotG Test: British Isles. Generated by tools/gen_history.py; do not edit.',
                 ' %s:0 "Off-Map"' % OFFMAP_GOVERNMENT,
                 ' %s_adjective:0 "Off-Map"' % OFFMAP_GOVERNMENT,
                 ' %s_realm:0 "Off-Map"' % OFFMAP_GOVERNMENT,
                 ' %s_desc:0 "TEST ONLY. Land outside the test zone. Nobody plays here; it only exists so the map has an edge."' % OFFMAP_GOVERNMENT,
                 ' %s_with_icon:0 "@government_type_herder! Off-Map"' % OFFMAP_GOVERNMENT,
                 ' eotg_test_bi_offmap_name:0 "Off-Map"']
        for k, txt in self.bookmark_loc:
            lines.append(' %s:0 "%s"' % (k, txt.replace('"', '\\"')))
        write_new(os.path.join(out, 'localization/english/eotg_test_bi_generated_l_english.yml'),
                  '\n'.join(lines) + '\n', bom=True)

    def write_readme_table(self):
        v = self.v
        rows = []
        for c in v.counties:
            z = self.zone_of(c)
            if z == 'offmap':
                continue
            h = self.holder_of(c)
            if h in self.new_chars:
                if z == 'mainland':
                    continue
                what = 'Unclaimed (Unsworn placeholder)'
                who = h
            else:
                gov = self.gov_of.get(h) or 'vanilla (%s)' % (self.v.state.get(c, {}).get('government') or 'default')
                who = '%s %s' % (h, (v.chars.get(h, {}) or {}).get('name') or '')
                top, x, seen = h, h, set()
                while x in self.liege_char and x not in seen:
                    seen.add(x)
                    x = self.liege_char[x]
                    top = x
                what = gov + ('' if top == h else ' (vassal of %s %s)' % (top, (v.chars.get(top, {}) or {}).get('name') or ''))
            rows.append((z, v.ancestors(c)[2], c, who.strip(), what))
        rows.sort()
        md = ['| Zone | Kingdom | County | Holder at 1066.9.15 | Government |', '|---|---|---|---|---|']
        for z, k, c, who, what in rows:
            md.append('| %s | %s | %s | %s | %s |' % (z, k, c, who, what))
        mainland_unsworn = sum(1 for c in v.counties if self.zone_of(c) == 'mainland' and self.holder_of(c) in self.new_chars)
        md.append('')
        md.append('Every other county of %s (%d) is an independent Unsworn county; every county outside '
                  'the zone (%d) belongs to one of %d offmap holders.' % (
                      ', '.join(e for e in ZONE_EMPIRES if e != ISLES_EMPIRE), mainland_unsworn,
                      sum(1 for c in v.counties if self.zone_of(c) == 'offmap'),
                      sum(1 for x in self.new_chars.values() if x['kind'] == 'offmap')))
        readme = os.path.join(SUB, 'README.md')
        if os.path.exists(readme):
            text = open(readme, encoding='utf-8').read()
            a, b = '<!-- BEGIN GENERATED TABLE -->', '<!-- END GENERATED TABLE -->'
            if a in text and b in text:
                pre, rest = text.split(a, 1)
                _, post = rest.split(b, 1)
                text = pre + a + '\n' + '\n'.join(md) + '\n' + b + post
                with open(readme, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(text)


# --------------------------------------------------------------- validation --
def validate(out):
    problems = []
    bad_key = re.compile(r'eotg_[ekdcb]_')
    for dirpath, _, files in os.walk(out):
        if os.sep + 'tools' in dirpath or dirpath.endswith('tools'):
            continue
        for f in files:
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, out).replace(os.sep, '/')
            if not f.endswith(('.txt', '.yml')):
                continue
            raw = open(full, 'rb').read()
            if raw.count(b'\xef\xbb\xbf') > 1 or (b'\xef\xbb\xbf' in raw and not raw.startswith(b'\xef\xbb\xbf')):
                problems.append('%s: BOM not exactly once at byte 0' % rel)
            if f.endswith('.yml'):
                if not raw.startswith(b'\xef\xbb\xbf'):
                    problems.append('%s: loc without BOM' % rel)
                continue
            text = raw[3:].decode('latin-1') if raw.startswith(b'\xef\xbb\xbf') else raw.decode('latin-1')
            try:
                top_entries(text)
                parse(text)
            except Exception as e:  # noqa
                problems.append('%s: %s' % (rel, e))
            if bad_key.search(text):
                problems.append('%s: contains an eotg_[ekdcb]_ key' % rel)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--game', default=DEFAULT_GAME)
    a = ap.parse_args()
    assert os.path.isdir(os.path.join(a.game, 'common/landed_titles')), 'not a CK3 game dir: %s' % a.game
    assert os.path.basename(SUB) == 'british_isles' and os.path.isfile(os.path.join(SUB, 'descriptor.mod'))
    for rel in GENERATED_DIRS:
        p = os.path.join(SUB, rel)
        if os.path.isdir(p):
            shutil.rmtree(p)
    for rel in GENERATED_FILES:
        p = os.path.join(SUB, rel)
        if os.path.exists(p):
            os.remove(p)

    print('reading vanilla from', a.game)
    v = Vanilla(a.game)
    b = Build(v, read_csv(os.path.join(SUB, 'isles_assignments.csv')),
              read_csv(os.path.join(SUB, 'bookmark_characters.csv')))
    b.assign()
    b.resolve()
    b.keep_set()
    b.write_titles(SUB)
    b.write_characters(SUB)
    b.write_provinces(SUB)
    b.write_wars(SUB)
    b.write_neutralised(SUB)
    b.write_bookmarks(SUB)
    b.write_challenge(SUB)
    b.write_trigger_override(SUB)
    b.write_loc(SUB)
    b.write_readme_table()

    kinds = collections.Counter(x['kind'] for x in b.new_chars.values())
    zone_counts = collections.Counter(b.zone_of(c) for c in v.counties)
    print('counties: isles %d, mainland %d, offmap %d' % (zone_counts['isles'], zone_counts['mainland'], zone_counts['offmap']))
    print('generated characters: %d Unsworn, %d offmap holders' % (kinds['unsworn'], kinds['offmap']))
    print('title history: %d files copied (replace_path), %d START blocks, %d titles in eotg_test_bi_titles.txt' % (
        len(v.title_files), sum(1 for k in b.final if b.block_for(k)), b.count_new_title_entries))
    print('characters: %d living kept, %d living retired (%d files overridden)' % (len(b.keep), len(b.retire), b.char_files_written))
    print('provinces: %d holding changes (%d files overridden)' % (len(b.prov_changes), b.prov_files_written))
    print('wars active at the start removed:', b.wars_removed)
    print('bookmark characters:', b.bookmark_listed)
    print('challenge characters kept:', b.challenge_kept)
    print('employer fixes:', b.employer_fix)
    print('not on the bookmark screen (no vanilla portrait; pick them on the map):', b.bookmark_skipped)
    print('isles cultures kept alive:', sorted(b.isles_cultures))
    print('trigger override lines added:', len(b.trigger_added))
    for n in b.notes:
        print('note:', n)
    problems = validate(SUB)
    for p in problems:
        print('VALIDATION:', p)
    for e in b.errors:
        print('ERROR:', e)
    if b.errors or problems:
        sys.exit(1)
    print('OK')


if __name__ == '__main__':
    main()
