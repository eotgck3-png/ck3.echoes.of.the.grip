"""Shared pieces for the mechanics models: world assumptions, agents, statistics.

Every number here that is not read from the mod's script is an ASSUMPTION and is
registered with assume(), so the report lists it. Models read the mod's own numbers
through pdx_read.Script, never from this file.
"""
import numpy as np
from pdx_read import Ctx, per_check_to_annual, VANILLA_DEFAULTS

ASSUMPTIONS = {}


def assume(key, value, why):
    ASSUMPTIONS[key] = (value, why)
    return value


# ---------------------------------------------------------------- world
# ASSUMPTION: personality frequencies (CK3 rulers carry ~3 of ~30 personality traits,
# so ~0.1 each); used only where a script trigger reads the trait.
TRAIT_FREQ = assume('trait_freq', {
    'greedy': 0.12, 'ambitious': 0.12, 'compassionate': 0.10, 'content': 0.10, 'craven': 0.10,
    'brave': 0.12, 'paranoid': 0.08, 'sadistic': 0.05, 'callous': 0.08, 'arbitrary': 0.08,
    'just': 0.10, 'honest': 0.10, 'arrogant': 0.10, 'cynical': 0.08, 'zealous': 0.10,
    'deceitful': 0.10,
}, 'about 1 in 10 per personality trait (3 traits of ~30)')

MORTALITY = assume('ruler_mortality_per_year', 0.035, 'mean reign about 28 years')
WAR_START = assume('war_start_per_year', 0.15, 'a realm enters a war 0.15/yr')
WAR_END = assume('war_end_per_year', 0.5, 'wars last about 2 years; ~23% of years at war')
BATTLES_PER_WAR_YEAR = assume('battles_per_war_year', 2.0, 'Poisson mean, as war leader')
BATTLE_WIN = assume('battle_win_chance', 0.5, 'even odds')
# ASSUMPTION: yearly gold income by highest held tier, and the share an AI keeps
INCOME = assume('gold_income_by_tier', {2: 25.0, 3: 60.0, 4: 150.0, 5: 300.0}, 'net yearly income')
SAVE_SHARE = assume('gold_saved_share', 0.35, 'the rest goes to vanilla spending (MAA, buildings)')
DEBT_SHOCK = assume('debt_shock_per_year', 0.06, 'chance a year ends in debt (war, ransom, overspend)')
# realm sizes: (top tier, list of vassal tiers)
SIZES = {1: (3, [2]), 4: (3, [2, 2, 2, 2]), 8: (4, [3, 3] + [2] * 6), 16: (4, [3] * 4 + [2] * 12)}
assume('realm_shapes', {k: v for k, v in SIZES.items()}, '1/4 vassals under a duke, 8/16 under a king, a quarter dukes')


class World:
    """Per-run random world state for a realm: wars, gold, traits, deaths."""

    def __init__(self, rng, runs, size):
        self.rng = rng
        self.runs = runs
        self.top_tier, vt = SIZES[size]
        self.vtiers = np.array(vt)
        self.nv = len(vt)
        self.at_war = np.zeros(runs, bool)
        self.top_gold = np.full(runs, INCOME[self.top_tier] * 1.0)
        self.v_gold = np.tile(np.array([INCOME[t] for t in vt], float), (runs, 1))
        self.top_traits = self.sample_traits((runs,))
        self.v_traits = self.sample_traits((runs, self.nv))

    def sample_traits(self, shape):
        return {t: self.rng.random(shape) < p for t, p in TRAIT_FREQ.items()}

    def step_war(self):
        start = self.rng.random(self.runs) < WAR_START
        end = self.rng.random(self.runs) < WAR_END
        self.at_war = np.where(self.at_war, ~end, start)

    def step_gold(self):
        self.top_gold += INCOME[self.top_tier] * SAVE_SHARE
        self.v_gold += np.array([INCOME[t] for t in self.vtiers]) * SAVE_SHARE
        shock = self.rng.random(self.runs) < DEBT_SHOCK
        self.top_gold = np.where(shock, -INCOME[self.top_tier] * 0.5, self.top_gold)
        vshock = self.rng.random((self.runs, self.nv)) < DEBT_SHOCK
        self.v_gold = np.where(vshock, -self.v_gold.clip(min=1) * 0.2, self.v_gold)

    def deaths(self, shape):
        return self.rng.random(shape) < MORTALITY

    def battles(self):
        k = np.where(self.at_war, self.rng.poisson(BATTLES_PER_WAR_YEAR, self.runs), 0)
        wins = self.rng.binomial(k, BATTLE_WIN)
        return wins, k - wins


def trait_ctx(traits, idx=None):
    return {('trait:' + t): (v if idx is None else v[:, idx]) for t, v in traits.items()}


def annual_take(R, d, ctx, tier_key, rng, shape):
    """AI policy: did the AI take decision d this year (per ai_check_interval and
    ai_will_do, gated by ai_potential)? Returns a bool array."""
    interval = d['interval'].get(tier_key, d['interval'].get('all', 0))
    if not interval:
        return np.zeros(shape, bool)
    pct = np.broadcast_to(np.asarray(R.ai_will_do(d, ctx), float), shape)
    pot = np.broadcast_to(np.asarray(R.ai_potential(d, ctx), bool), shape)
    p = per_check_to_annual(pct, interval)
    return (rng.random(shape) < p) & pot


TIER_KEY = {2: 'county', 3: 'duchy', 4: 'kingdom', 5: 'empire'}


# ---------------------------------------------------------------- statistics
def series_stats(x, lo=0.0, hi=100.0):
    """x: (runs, years). Quantiles per year, share of run-years at each clamp,
    equilibrium (median of the last 20 years) and the first year the rolling
    median stays within 5% of the range of it."""
    q = np.percentile(x, [10, 50, 90], axis=0)
    at_lo = float(np.mean(x <= lo + 1e-9))
    at_hi = float(np.mean(x >= hi - 1e-9))
    eq = float(np.median(x[:, -20:]))
    med = q[1]
    tol = 0.05 * (hi - lo)
    settle = None
    for y in range(len(med)):
        if np.all(np.abs(med[y:] - eq) <= tol):
            settle = y
            break
    # runaway / dead: 20+ consecutive years at a clamp
    def streak(mask):
        best = np.zeros(x.shape[0], int)
        cur = np.zeros(x.shape[0], int)
        for y in range(x.shape[1]):
            cur = np.where(mask[:, y], cur + 1, 0)
            best = np.maximum(best, cur)
        return float(np.mean(best >= 20))
    return {'p10': q[0], 'p50': q[1], 'p90': q[2], 'at_lo': at_lo, 'at_hi': at_hi,
            'equilibrium': eq, 'settle_year': settle,
            'runaway_hi_20y': streak(x >= hi - 1e-9), 'dead_lo_20y': streak(x <= lo + 1e-9)}


def fmt_pct(v):
    return f'{100 * v:.1f}%'
