import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trade_variants as T
import numpy as np, common
import trade_variants as T
from pdx_read import Script
# monkeypatch: war-year-only dues via a wrapper around run
def run_waronly(R, size, pol, runs, years, seed, d):
    # war-year dues with >=1 peaceful vassal == top war loss of (war + d) when a peaceful vassal exists.
    # Approximate: with 1-16 vassals at 3% own-war, P(no peaceful vassal) ~ 0, so use top_war = war + d.
    return T.run(R, size, pol, runs, years, seed, top_war=R.num('eotg_gobcorp_war_loss_value') + d)
R = Script()
for name, f in (('E war-dues +1 (net -3 top)', lambda s,p: run_waronly(R,s,p,2000,100,20261103,1)),
                ('D war-dues +2 (net -2 top)', lambda s,p: run_waronly(R,s,p,2000,100,20261103,2)),
                ('F dues +0.5 every year', lambda s,p: T.run(R,s,p,2000,100,20261103,dues=0.5)),
                ('G war-dues +2 & squeeze -3', lambda s,p: T.run(R,s,p,2000,100,20261103,top_war=-2.0,corner_squeeze=-3))):
    for s in (1,4,16):
        for p in ('ai','greedy'):
            print(name, s, p, f(s,p), flush=True)
base = common.WAR_START
for share in (0.10,0.20,0.30,0.40):
    common.WAR_START = 0.5*share/(1-share)
    print('sweep', share, 'F', T.run(R,4,'ai',2000,100,20261103,dues=0.5), flush=True)
common.WAR_START = base
