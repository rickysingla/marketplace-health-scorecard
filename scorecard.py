"""Marketplace health scorecard on synthetic data.

Builds 26 weeks of two-sided marketplace data (sellers, listings,
buyers, orders), then computes the handful of ratios that tell you
whether the marketplace is actually healthy — including a segment
where engagement rises while long-term value falls.

Pure standard library. Run:  python3 scorecard.py
"""

import random
import statistics

random.seed(7)

WEEKS = 26


def gen_weeks() -> list[dict]:
    weeks = []
    sellers = 1_200
    for w in range(WEEKS):
        sellers = int(sellers * 1.03)                      # supply grows 3%/wk
        listings = sellers * random.uniform(18, 22)
        buyers = int(50_000 * (1.02 ** w))                 # demand grows 2%/wk
        # a promo from week 14 brings in low-intent buyers:
        promo = w >= 14
        orders = buyers * (0.16 if promo else 0.18)        # conversion dips
        repeat_rate = 0.31 if promo else 0.38              # repeat share drops
        weeks.append({
            "week": w + 1,
            "sellers": sellers,
            "listings": int(listings),
            "buyers": buyers,
            "orders": int(orders),
            "repeat_rate": repeat_rate,
            "promo": promo,
        })
    return weeks


def scorecard(weeks: list[dict]) -> None:
    print(f"{'Wk':>3}{'Sellers':>9}{'Listings':>10}{'Buyers':>9}"
          f"{'Orders':>9}{'Orders/seller':>15}{'Repeat%':>9}")
    for wk in weeks:
        print(f"{wk['week']:>3}{wk['sellers']:>9,}{wk['listings']:>10,}"
              f"{wk['buyers']:>9,}{wk['orders']:>9,}"
              f"{wk['orders'] / wk['sellers']:>15.1f}{wk['repeat_rate']:>9.0%}")


def diagnose(weeks: list[dict]) -> None:
    pre = [w for w in weeks if not w["promo"]]
    post = [w for w in weeks if w["promo"]]
    avg = lambda rows, k: statistics.mean(r[k] for r in rows)
    print("\nBefore promo (wks 1-13) vs during promo (wks 14-26):")
    print(f"  Orders/week:      {avg(pre, 'orders'):>10,.0f} -> {avg(post, 'orders'):>10,.0f}  (up)")
    print(f"  Orders/seller:    {avg(pre, 'orders') / avg(pre, 'sellers'):>10.1f} -> "
          f"{avg(post, 'orders') / avg(post, 'sellers'):>10.1f}  (down: supply outgrows demand)")
    print(f"  Repeat rate:      {avg(pre, 'repeat_rate'):>10.0%} -> {avg(post, 'repeat_rate'):>10.0%}  (down)")
    print("\nFlag: engagement (orders) is up, but orders per seller and repeat")
    print("rate are both down. That is the classic pattern of buying growth")
    print("with low-intent demand — headline metrics improve while the")
    print("marketplace gets weaker. Check cohort LTV before scaling the promo.")


def main() -> None:
    weeks = gen_weeks()
    scorecard(weeks)
    diagnose(weeks)


if __name__ == "__main__":
    main()
