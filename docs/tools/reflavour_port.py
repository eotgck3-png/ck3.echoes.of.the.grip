"""Port v1's vanilla-UI reflavour layer into v2 (docs/specs/reflavour_v2.md).

    python docs/tools/reflavour_port.py            # dry run: counts only
    python docs/tools/reflavour_port.py --write    # (re)write localization/english/replace/eotg_reflavour_*.yml
                                                   # and docs/specs/reflavour_v2_held_keys.md is NOT regenerated

Reads OLD PROJECT VERSION/localization/english/replace/*.yml and the v2 localization/ tree.
Ports v1 TERM keys only (no event prose), applies County/Region -> Shoal outside [..], $..$ and #fmt
tokens, and holds a key that is: in a blocked file or key (pending rulings), already defined in v2,
a conflicting v1 duplicate, event prose, or still carrying a medieval/Earth word. House-style fixes
(Canadian spelling, dashes, quotes) were applied by hand after the first run and are NOT redone here:
re-running --write overwrites them, so re-apply or extend this tool first. Edit BLOCKED_FILES /
BLOCKED_KEYS when a glossary ruling lands.
"""
import re, glob, os, sys, collections, json
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V1=os.path.join(ROOT,'OLD PROJECT VERSION/localization/english/replace')
LINE=re.compile(r'^\s*([^\s#:"]+):(\d*)\s*"(.*)"\s*(?:#.*)?$')
def parse(path):
    out=[]
    for i,l in enumerate(open(path,encoding='utf-8-sig'),1):
        m=LINE.match(l.rstrip('\n'))
        if m: out.append((m.group(1),m.group(3),i))
    return out
v1={}
occ=collections.defaultdict(list)
for f in sorted(glob.glob(V1+'/*.yml')):
    for k,v,i in parse(f):
        occ[k].append((os.path.basename(f),v,i))
v2=collections.defaultdict(list)
for f in glob.glob(os.path.join(ROOT,'localization/**/*.yml'),recursive=True):
    if os.path.basename(f).startswith('eotg_reflavour_'): continue  # this tool's own output
    for k,v,i in parse(f): v2[k].append(os.path.relpath(f,ROOT))
total=len(occ); dup=[k for k,o in occ.items() if len(o)>1]
conf=[k for k in dup if len({v for _,v,_ in occ[k]})>1]
inv2=[k for k in occ if k in v2]


occ=dict(occ); v2=dict(v2)
BLOCKED_FILES={ # pending rulings (glossary_proposal_cloud.md §3, §5.4)
 'eotg_terrains_l_english.yml':'terrain names pending the tier-vs-terrain ruling (glossary §3.2, §6.1 items 5-7)',
 'eotg_custom_loc_wordbank_l_english.yml':'must change in sync with the terrain names (glossary §3.2, localization_crusade.md:136-141)',
 'eotg_traditions_l_english.yml':'blocked until the terrain ruling, and uses "Void" for ordinary space (glossary §3.2, §5.4)',
}
BLOCKED_KEYS={'horse_archers_lowercase':'as horse_archers (glossary §5.6)','horse_archers':'"Strike Speeders" clashes with the mod\'s own eotg_maa_strike_speeders (glossary §5.6, §6.1 item 12)',
              'horse_archers_flavor':'as horse_archers (glossary §5.6)'}
def is_event(k): return bool(re.search(r'\.\d{2,5}(\b|\.|$)',k))
SEG=re.compile(r'(\[[^\]]*\]|\$[^$]*\$|#[A-Za-z_]+\b|#!)')
def outside(v, fn):
    parts=SEG.split(v)
    return ''.join(p if SEG.fullmatch(p) else fn(p) for p in parts)
def strip(v): return re.sub(r'\[[^\]]*\]|\$[^$]*\$','',v)
SUBS=[(r'\bCounties\b','Shoals'),(r'\bcounties\b','Shoals'),(r'\bCounty\b','Shoal'),(r'\bcounty\b','Shoal'),
      (r'\bRegions\b','Shoals'),(r'\bregions\b','Shoals'),(r'\bRegion\b','Shoal'),(r'\bregion\b','Shoal')]
def transform(v):
    def f(t):
        for a,b in SUBS: t=re.sub(a,b,t)
        return t
    return outside(v,f)
MEDIEVAL=r"castles?|peasants?|serfs?|knights?|knighted|horses?|wheat|spears?|rice|forests?|forester|villages?|villagers?|lords?|lordling|ladies|crops?|swords?|harvest|kings?|queens?|emperors?|empires?|church(es)?|monaster\w*|fief\w*|manor\w*|plow|plough|pope|bishops?|abbey|kingdoms?|duch(y|ies)|baron(y|ies)|temples?|tribes?\w*|pitchforks?|archers?|axes?|joust\w*|windmill|maund|dung\w*|arrows?|cavalry|steeds?|saddle\w*|mounts?|chivalr\w*|feudal|medieval|god|gods|goddess"
EARTH=r"roman|rome|muslims?|islam\w*|christian\w*|persian|persia|sicily|german\w*|burgund\w*|shiva|ganga|britannia|toledo|premysl|stadice|meteora|europe\w*|byzant\w*|norse|viking\w*|jesus|catholic|pagan|saxon|frank\w*|india\w*|chin(a|ese)|mongol\w*|arab\w*"
BAD=re.compile(r'\b('+MEDIEVAL+'|'+EARTH+r')\b',re.I)
held=collections.OrderedDict(); ported=collections.defaultdict(list); reasons=collections.Counter()
seen=set()
for k,o in occ.items():
    f0=o[0][0]
    def hold(r):
        held[k]=(f0,r); reasons[r.split(':')[0]]+=1
    if f0 in BLOCKED_FILES: hold('blocked file: '+BLOCKED_FILES[f0]); continue
    if k in BLOCKED_KEYS: hold('blocked key: '+BLOCKED_KEYS[k]); continue
    if k in v2: hold('already defined in v2: '+', '.join(v2[k])); continue
    vals={v for _,v,_ in o}
    if len(vals)>1: hold('conflicting duplicate in v1: '+', '.join(f'{a}:{c}' for a,_,c in o)); continue
    if is_event(k): hold('event prose: held (vanilla 1.19 event text, stale-scope risk, residual medieval prose)'); continue
    v=transform(o[0][1])
    if '[scope:' in v: hold('uses [scope:'); continue
    if re.search(r'gob-?corp',v,re.I): hold('says Gob-Corp'); continue
    m=BAD.search(strip(v))
    if m: hold(f'medieval or Earth word: "{m.group(0)}"'); continue
    ported[f0].append((k,v,o[0][1]!=v))
d={'held':held,'ported':ported}
print('ported',sum(len(x) for x in ported.values()),'held',len(held))
for r,c in reasons.most_common(): print(f'  {c:4d} {r}')
if "--write" in sys.argv:
    
    out=os.path.join(ROOT,'localization/english/replace')
    written=[]
    for f,rows in sorted(d['ported'].items()):
        area=f[len('eotg_'):-len('_l_english.yml')]
        name=f'eotg_reflavour_{area}_l_english.yml'
        lines=['l_english:',
          f'# Vanilla-UI reflavour, ported from v1 (OLD PROJECT VERSION/localization/english/replace/{f}).',
          '# UNVERIFIED-VANILLA: keys ported from v1 (CK3 1.19); the local session diffs them against 1.20.1.1',
          '# Spec: docs/specs/reflavour_v2.md. County tier = Shoal (owner ruling 2026-10-20). One definition per key across',
          '# localization/, replace/ included: county keys stay in eotg_county_term_l_english.yml. Held keys are listed in the spec.',
          '']
        for k,v,_ in rows: lines.append(f' {k}:0 "{v}"')
        open(os.path.join(out,name),'w',encoding='utf-8-sig',newline='\n').write('\n'.join(lines)+'\n')
        written.append((name,len(rows)))
    for n,c in written: print(c,n)
    print(len(written),'files')
