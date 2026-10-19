# -*- coding: utf-8 -*-
"""
paper_GPCR Fig. 3 (fig3_atlas_repair.png)  -  Atlas-wide distributions,
robustness and repair.
Adapted from 04_code/ed_scripts/edfig12.py (cell-communication-audit repo):
suptitle removed for the standalone paper; panel-a annotation corrected to
entry-level quantiles computed from the plotted histogram data (the previous
annotation quoted pair-level proxy quantiles from the summary JSON).
Run: python make_fig3.py   (writes fig3_atlas_repair.png next to this script)
"""
import json, sys, os
import numpy as np
import pandas as pd
EDSCRIPTS = HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, EDSCRIPTS)
from edstyle import setup, panel_label, OI
import matplotlib.pyplot as plt

setup()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AT = os.path.join(ROOT, "results", "atlas_audit")

entries = pd.read_csv(os.path.join(AT, "atlas_audit_entries.csv"))
groups = pd.read_csv(os.path.join(AT, "atlas_audit_groups.csv"))
papers = pd.read_csv(os.path.join(AT, "atlas_audit_papers.csv"))
repair = pd.read_csv(os.path.join(AT, "atlas_repair_projection.csv"))
frac = pd.read_csv(os.path.join(AT, "atlas_fracture_probability.csv"))

fig, axs = plt.subplots(2, 3, figsize=(7.2, 4.8))
axs = axs.ravel()

# ---- a: entry-level deviation distribution ----
ax = axs[0]
dev = entries["dev_entry"].abs().dropna().values
bins = np.logspace(-3, 1.2, 60)
ax.hist(dev, bins=bins, color=OI["blue"], alpha=0.85)
ax.axvline(0.3, color=OI["verm"], ls="--", lw=0.8)
ax.axvline(1.0, color=OI["verm"], ls=":", lw=0.8)
ymax = ax.get_ylim()[1]
ax.text(0.31, ymax*0.8, "0.3 dex", fontsize=5, color=OI["verm"])
ax.text(1.02, ymax*0.6, "1 dex", fontsize=5, color=OI["verm"])
ax.set_xscale("log")
ax.set_xlabel(r"|$\Delta$log($\tau$/K$_A$) - $\Delta$log(E$_{max}$/EC$_{50}$)|  (dex, per entry)")
ax.set_ylabel("entries")
ax.set_title("entry-level deviations")
qe = np.percentile(dev, [50, 90, 99])
ax.text(0.97, 0.97, f"entry quantiles:\nP50 {qe[0]:.2f}  P90 {qe[1]:.2f}\nP99 {qe[2]:.2f} dex",
        transform=ax.transAxes, fontsize=5, va="top", ha="right", color="0.35")

# ---- b: per-paper medians ----
ax = axs[1]
pm = papers["dev_median"].sort_values().values
ax.plot(np.arange(1, len(pm) + 1), pm, "o", ms=2.5, color=OI["blue"])
ax.axhline(0.3, color=OI["verm"], ls="--", lw=0.8)
ax.set_yscale("log")
ax.set_xlabel("paper (rank, 66 multi-ligand papers)")
ax.set_ylabel("median |deviation| (dex)")
ax.set_title("per-paper medians")
n_exc = (pm > 0.3).sum()
ax.text(2, 0.35, f"{n_exc} papers above line", fontsize=5, color=OI["verm"])

# ---- c: repair-cost distribution ----
ax = axs[2]
cost = repair["cost_rms_dex"].dropna().values
bins = np.logspace(-3, 1.2, 50)
counts, _, _ = ax.hist(cost, bins=bins, color=OI["green"], alpha=0.85)
ax.set_ylim(0, counts.max() * 1.22)
top = ax.get_ylim()[1]
ax.axvline(0.072, color="0.3", ls="-", lw=0.8)
ax.text(0.066, top * 0.92, "median 0.072", fontsize=5, color="0.3", ha="right")
ax.axvline(0.3, color=OI["verm"], ls="--", lw=0.8)
ax.text(0.34, top * 0.78, "24.2% > 0.3", fontsize=5, color=OI["verm"], ha="left")
ax.set_xscale("log")
ax.set_xlabel("group repair cost, RMS (dex)")
ax.set_ylabel("assay groups")
ax.set_title("repair cost")

# ---- d: repair move vs fracture probability ----
ax = axs[3]
ax.plot(np.abs(frac["repair_move"]), frac["p_broken"], ".", ms=1.5, color=OI["pink"], alpha=0.4)
ax.set_xscale("log")
ax.set_xlabel("|repair move| per entry (dex)")
ax.set_ylabel("fracture probability")
ax.set_title("cost vs fracture probability")
ax.text(0.03, 0.97,
        "15.0% of entries p > 0.9\n"
        "vs 14.5% with |dev| > 0.3 dex\n"
        "mixture: pi_h 0.745,\nsigma_h 0.089, sigma_b 0.683",
        transform=ax.transAxes, fontsize=4.6, va="top", color="0.35", linespacing=1.25)

# ---- e: threshold robustness ----
ax = axs[4]
thr = [0.2, 0.3, 0.5, 0.8, 1.0]
grp = [39.03, 26.02, 14.87, 7.81, 5.20]
pap = [37.88, 22.73, 13.64, 6.06, 3.03]
ax.plot(thr, grp, "o-", color=OI["blue"], ms=4, label="groups (269)")
ax.plot(thr, pap, "s--", color=OI["verm"], ms=4, label="papers (66)")
for x, y in zip(thr, grp):
    ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 4), fontsize=5,
                color=OI["blue"], ha="center")
ax.set_ylim(0, 46)
ax.set_xlabel("deviation threshold (dex)"); ax.set_ylabel("exceedance rate (%)")
ax.set_title("threshold robustness")
ax.legend(fontsize=5.5)

# ---- f: robustness checks ----
ax = axs[5]
cats = ["neg. control\n(Hb)", "aggregation\nrho 0-0.5", "conservative\nSIG=0.10", "jackknife"]
vals = [0, 55.6, 28.2, 65.7]
cols = [OI["green"], OI["blue"], OI["sky"], OI["orange"]]
bars = ax.bar(range(4), vals, color=cols, width=0.62)
notes = ["0/5 alarms\np50 spread\n0.007 dex", "134/241\ngroups", "68/241\ngroups", "65.7% flagged\nGIRK jack. = 1.0"]
for b, v, n_ in zip(bars, vals, notes):
    ax.text(b.get_x() + b.get_width()/2, v + 1.5, n_, ha="center", fontsize=4.8)
ax.set_xticks(range(4), cats, fontsize=5.5, rotation=18, ha="right")
ax.set_ylabel("%")
ax.set_title("robustness checks")
ax.set_ylim(0, 85)

for i, ax in enumerate(axs):
    panel_label(ax, "abcdef"[i], x=(-0.21 if i == 0 else -0.15), y=1.06)

fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3_atlas_repair.png"), bbox_inches="tight", dpi=300)
fig.savefig(os.path.join(HERE, "fig3_atlas_repair.pdf"), bbox_inches="tight")
print("saved fig3_atlas_repair.png / .pdf")
