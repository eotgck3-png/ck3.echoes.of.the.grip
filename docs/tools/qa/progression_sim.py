"""Monte-Carlo of years until a tier's progression event fires and is accepted.

Models one yearly random_list: total eligible weight W, the progression
branch's weight, a "nothing" weight, a cooldown (in pulses) after any event,
and an acceptance chance. Read the weights off the tier's random_list in
common/on_action/eotg_augmentation_on_actions.txt; the defaults are the
2026-10-03 values (tier 1: The Upgrade 30 of ~240 eligible, nothing 150).
Prints median years, and the share that progressed within 10 and 20 years.
Needs no repo files.
"""
import argparse
import random
import statistics


def simulate(total_weight, prog_weight, nothing, cooldown, accept, runs, cap):
    years_list = []
    for _ in range(runs):
        years, cd = 0, 0
        while years < cap:
            years += 1
            if cd > 0:
                cd -= 1
                continue
            if random.random() * (total_weight + nothing) < total_weight:
                cd = cooldown
                if random.random() < prog_weight / total_weight and random.random() < accept:
                    break
        years_list.append(years)
    return (statistics.median(years_list),
            sum(1 for y in years_list if y <= 10) / runs,
            sum(1 for y in years_list if y <= 20) / runs)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--total", type=float, default=240, help="sum of eligible branch weights (excl. nothing)")
    p.add_argument("--prog", type=float, default=30, help="progression branch weight")
    p.add_argument("--nothing", type=float, default=150, help="nothing-branch weight")
    p.add_argument("--cooldown", type=int, default=2, help="pulses skipped after any event (2-year flag = 2)")
    p.add_argument("--accept", type=float, nargs="+", default=[1.0, 0.45],
                   help="acceptance chance(s) to test, e.g. 1.0 for a player who always accepts")
    p.add_argument("--runs", type=int, default=20000)
    p.add_argument("--cap", type=int, default=80, help="give up after this many years")
    a = p.parse_args()
    for acc in a.accept:
        med, by10, by20 = simulate(a.total, a.prog, a.nothing, a.cooldown, acc, a.runs, a.cap)
        print(f"accept={acc}: median {med} years, {by10:.0%} within 10y, {by20:.0%} within 20y")


if __name__ == "__main__":
    main()
