# marketplace-health-scorecard

The few ratios that tell you whether a two-sided marketplace is healthy, computed on synthetic data.

## Problem

Marketplace dashboards usually lead with totals: orders, buyers, listings. Totals almost always go up, including when the marketplace is getting worse — supply growing faster than demand, or a promotion pulling in buyers who never come back. By the time totals fall, the damage is quarters old.

## Approach

`scorecard.py` generates 26 weeks of synthetic marketplace data, then computes:

- **Orders per seller** — the supply/demand balance. If sellers grow faster than orders, each seller earns less and churn follows.
- **Repeat rate** — the share of demand that comes back. New-buyer spikes with falling repeat rates are rented growth, not earned growth.
- A before/after **diagnosis** of a week-14 promotion that lifts orders while both health ratios deteriorate.

## What the code shows

A worked example of the "engagement up, value down" trap: the promo makes the headline metric better and the marketplace worse at the same time. The scorecard's job is to make that visible in one screen, early enough to act on.

## Run

```bash
python3 scorecard.py
```

Standard library only. All data is synthetic.
