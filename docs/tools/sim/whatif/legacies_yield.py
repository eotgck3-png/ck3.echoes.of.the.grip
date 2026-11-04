import os, sys
SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, 'models'))
import legacies as L
from pdx_read import Script
R = Script(repo=L.V1)
y = L.survey_seed_yield(R)
print('repo yield', y)
# hand recompute with 0002.a seeding branches halved (30,25 -> 15,12.5; gold 25 and unstable 20 unchanged)
t2 = L.option_table(R, '0002'); t3 = L.option_table(R, '0003')
w2 = {o['name']: o['weight'] for o in t2}; print('0002 weights', w2); print('0003 weights', {o['name']: o['weight'] for o in t3})
def y2(a_seed):
    W = sum(w2.values()); return w2['eotg_legacy_0002_opt_excavate']/W*a_seed + w2['eotg_legacy_0002_opt_recalculate']/W*0.70
p3 = y['per_event']['0003']['p_new_site']
for label, a_seed, fb in [('as is', 75/100, (0.4, 0.4, 0.2)), ('0002.a branches halved', 47.5/72.5, (0.4, 0.4, 0.2)),
                          ('fallback 0002/0003 weights halved', 75/100, (40/70, 20/70, 10/70)),
                          ('every seeding branch wrapped in 50% chance', 75/100*0.5, (0.4, 0.4, 0.2))]:
    yy = fb[1]*y2(a_seed) + fb[2]*p3
    if label.startswith('every'):
        yy = fb[1]*(y2(75/100)*0.5) + fb[2]*p3*0.5
    print(f'{label}: yield {yy:.3f}; player-century (20 surveys) {20*yy:.2f}; AI ruler-century (6.9 surveys) {6.9*yy:.2f}')
