# -*- coding: utf-8 -*-
"""
code72b_null_at_fixed_cut.py
============================================================
Companion to code72: the identity-1 null at FIXED deviation cuts,
at both the entry level and the pair level.

Why this file exists
--------------------
code72 M1 measures the false-positive rate under the detector's own
rule, |dev| > max(0.3, 2 sigma). That rule is not the rule used for the
Atlas census, which counts |dev| > 0.3 dex (and > 1 dex) at a fixed cut.
Comparing a fixed-cut observed rate to a max-rule null rate mixes two
thresholds. This script puts the null on the same fixed cuts.

It also puts the null on the same *unit*. code72 M1 scores entries
(one ligand x one assay); the Atlas census scores pairs (the difference
of two entry residuals inside one assay group). A pair difference is
about sqrt(2) wider than an entry residual, so the two rates are not
comparable without this step.

Null model (identical to code72 M1)
-----------------------------------
True model self-consistent; SEM at the anchor datasets' reported
magnitude: pEC50 +-0.2, log tau +-0.2, Emax +-5, log(tau/KA) +-0.15.
Seed 20260816, 2000 simulations x 5 ligands x 6 assay arms.

Residual scored here
--------------------
r = log(tau/KA) - [log tau + pEC50 - log10(1 + tau)]   (code66 identity 2)
entry deviation  = |r|
pair  deviation  = |r_i - r_j| for two ligands inside one assay arm

Output
------
Entry-level and pair-level exceedance rates at the fixed cuts used in
the Atlas census, to be compared with the archived distribution
(atlas_audit_entries.csv / atlas_pair_violations.csv).

Run: python code72b_null_at_fixed_cut.py
============================================================
"""
import itertools
import numpy as np

SEED = 20260816
NSIM, NLIG, NARM = 2000, 5, 6
CUTS = (0.3, 0.5, 0.57, 1.0)

rng = np.random.default_rng(SEED)

entry = []
for _ in range(NSIM):
    block = np.empty((NLIG, NARM))
    for lig in range(NLIG):
        pKA = rng.uniform(6, 9)
        for arm in range(NARM):
            tau = 10 ** rng.uniform(-0.7, 2.0)
            pEC50_true = pKA + np.log10(1 + tau)
            lt_true = np.log10(tau)
            lr_true = lt_true + pKA
            em = np.clip(100 * tau / (1 + tau) + rng.normal(0, 5.0), 1, 99)
            pec = pEC50_true + rng.normal(0, 0.2)
            lt = lt_true + rng.normal(0, 0.2)
            lr = lr_true + rng.normal(0, 0.15)
            pred = lt + pec - np.log10(1 + 10 ** lt)
            block[lig, arm] = lr - pred
    entry.append(block)

signed = np.stack(entry)                           # (NSIM, NLIG, NARM), signed r
entry_dev = np.abs(signed)
pair_dev = np.abs(np.stack([
    signed[:, i, :] - signed[:, j, :]
    for i, j in itertools.combinations(range(NLIG), 2)
], axis=1))                                        # (NSIM, NPAIR, NARM)

print("=" * 78)
print("null exceedance rates at fixed cuts (seed %d, %d sims)" % (SEED, NSIM))
print("=" * 78)
print("%-8s %12s %12s" % ("cut", "entry", "pair"))
for c in CUTS:
    print("%-8.2f %12.4f %12.4f" % (c, (entry_dev > c).mean(), (pair_dev > c).mean()))
print()
print("cells per level: entry %d, pair %d" % (entry_dev.size, pair_dev.size))
print()
print("For comparison, the archived distribution")
print("  entry level (atlas_audit_entries.csv):")
print("    >0.3 0.145   >0.5 0.074   >1.0 0.023")
print("  pair level (atlas_pair_violations.csv):")
print("    >0.3 0.215   >0.5 0.114   >0.57 0.094   >1.0 0.042")
print()
print("Reading: below ~0.5 dex the archive is TIGHTER than this null;")
print("beyond 1 dex it is far heavier. The inconsistency is a tail,")
print("not a uniform property of the record.")
