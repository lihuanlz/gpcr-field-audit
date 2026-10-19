# -*- coding: utf-8 -*-
"""
paper_GPCR Fig. 2 (fig2_fracture_maps.png)  -  per-study fracture maps.
Adapted from 04_code/ed_scripts/edfig11.py (cell-communication-audit repo):
suptitle removed for the standalone paper; panel-a title corrected to describe
the plotted quantity (cross-arm spread) instead of the CI-cAMP gap.
Data transcribed from code 63/65/66/69 run outputs; code-80 posterior CSV.
Run: python make_fig2.py   (writes fig2_fracture_maps.png next to this script)
"""
import sys, os
import numpy as np
import pandas as pd
EDSCRIPTS = HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, EDSCRIPTS)
from edstyle import setup, panel_label, OI
import matplotlib.pyplot as plt

setup()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

fig, axs = plt.subplots(2, 3, figsize=(7.2, 4.8))
axs = axs.ravel()

# ---- a: D2R pKA(arm,time) cross-arm spread (code 69) ----
ax = axs[0]
tmin = [2, 5, 10, 15, 30, 45, 60, 75, 90]
spread = {
    "Ropinirole":  [1.36, 1.27, 0.93, 0.64, 0.31, 0.70, 0.89, 0.58, 0.70],
    "Dopamine":    [1.14, 0.92, 0.18, 0.54, 0.75, 0.74, 1.00, 0.14, 1.30],
    "Aripiprazole":[1.30, 1.65, 1.56, 1.58, 1.49, 1.87, 1.97, 2.69, 2.31],
    "Cariprazine": [1.33, 1.54, 1.54, 1.47, 1.45, 1.44, 1.51, 1.56, 1.77],
    "Bifeprunox":  [1.32, 1.17, 1.35, 1.35, 1.43, 1.56, 1.50, 1.93, 1.78],
    "Pardoprunox": [1.66, 1.70, 1.32, 1.27, 1.00, 1.35, 1.35, 1.29, 1.37],
    "S-3PPP":      [1.38, 1.36, 1.48, 1.57, 1.44, 1.75, 1.80, 1.74, 1.91],
}
for lig, v in spread.items():
    hl = lig in ("Bifeprunox", "Aripiprazole", "Cariprazine")
    ax.plot(tmin, v, "o-", ms=2.5, lw=1.2 if hl else 0.6,
            color={"Bifeprunox": OI["verm"], "Aripiprazole": OI["blue"],
                   "Cariprazine": OI["sky"]}.get(lig, "0.65"),
            label=lig if hl else None)
ax.set_xlabel("readout time (min)"); ax.set_ylabel(r"cross-arm pK$_A$ spread (dex)")
ax.set_title("D2R cross-arm pK$_A$ spread over readout time")
ax.legend(fontsize=5.5)

# ---- b: D2R binding-vs-function fracture (code 63) ----
ax = axs[1]
ligs = ["Dopamine", "Ropinirole", "Aripiprazole", "Cariprazine", "Bifeprunox", "Pardoprunox", "S-3PPP"]
import json as _json
_D2 = _json.load(open(os.path.join(ROOT, "results", "derived", "code63_d2r.json"),
                      encoding="utf-8"))["test2"]
dc_amp, dc_gao = {}, {}
for _l in ligs:
    _c, _g = _D2[_l]["cAMP"], _D2[_l]["GaoB"]
    if _c.get("status") == "ok":
        dc_amp[_l] = (_c["delta"], _c["sd"])
    if _g.get("status") == "ok":
        dc_gao[_l] = (_g["delta"], _g["sd"])
xx = np.arange(len(ligs))
for i, lig in enumerate(ligs):
    if lig in dc_amp:
        ax.errorbar(i - 0.12, dc_amp[lig][0], yerr=dc_amp[lig][1], fmt="o", ms=4,
                    color=OI["blue"], elinewidth=0.6, capsize=1.5)
        ax.errorbar(i + 0.12, dc_gao[lig][0], yerr=dc_gao[lig][1], fmt="s", ms=4,
                    color=OI["verm"], elinewidth=0.6, capsize=1.5)
    else:
        ax.text(i, 0.4, "tau -> inf\n(full agonist,\nunresolvable)", ha="center", fontsize=4.5, color="0.45")
ax.axhline(0, color="0.5", lw=0.5)
ax.plot([], [], "o", color=OI["blue"], label="cAMP arm")
ax.plot([], [], "s", color=OI["verm"], label="GaoB arm")
ax.set_xticks(xx, ligs, rotation=30, ha="right", fontsize=5.5)
ax.set_ylabel(r"pK$_{A,func}$ - pK$_i$ (dex)")
ax.set_title("D2R binding-versus-function fracture")
ax.legend(fontsize=5.2, loc="lower left")
ax.set_ylim(-4.2, 2.0)

# ---- c: CI - cAMP time evolution + bias reversal ----
ax = axs[2]
cicamp = {
    "Aripiprazole": [0.86, 1.33, 1.52, 1.58, 1.41, 1.87, 1.97, 2.02, 2.22],
    "Cariprazine":  [1.10, 1.32, 1.42, 1.44, 1.39, 1.44, 1.51, 1.56, 1.77],
    "Bifeprunox":   [0.74, 1.17, 1.35, 1.35, 1.27, 1.52, 1.50, 1.57, 1.68],
    "Pardoprunox":  [0.60, 0.99, 1.16, 1.27, 1.00, 1.35, 1.35, 1.29, 1.37],
    "S-3PPP":       [0.86, 1.19, 1.48, 1.57, 1.44, 1.75, 1.80, 1.74, 1.91],
}
cols = {"Aripiprazole": OI["blue"], "Cariprazine": OI["sky"], "Bifeprunox": OI["verm"],
        "Pardoprunox": "0.6", "S-3PPP": "0.6"}
for lig, v in cicamp.items():
    ax.plot(tmin, v, "o-", ms=2.5, lw=1.2 if lig == "Bifeprunox" else 0.6,
            color=cols[lig], label=lig if lig != "Pardoprunox" else None)
ax.set_xlabel("readout time (min)"); ax.set_ylabel(r"pK$_{A,CI}$ - pK$_{A,cAMP}$ (dex)")
ax.set_title("D2R: CI - cAMP grows with time")
ax.legend(fontsize=5.2, loc="upper left")
ax.text(88, 0.62, "bias factor bifeprunox vs ropinirole:\n-0.42 dex (2 min) -> +1.93 dex (90 min);\nbifeprunox 0.91 dex off at best; S-3PPP +1.49 reverse",
        fontsize=5, color="0.35", ha="right", va="bottom")

# ---- d: AT1R cross-arm fracture (code 65) ----
import json as _json
_A1 = _json.load(open(os.path.join(ROOT, "results", "derived", "code65_at1r.json"),
                      encoding="utf-8"))["test_a"]
ax = axs[3]
rows = []
for _lab, _cond in [("TRV026 WT", "WT"), ("TRV026 L112A", "L112A"), ("TRV026 Y292A", "Y292A")]:
    _r = _A1[_cond]["TRV026"]
    rows.append((_lab, _r["delta"], float(np.hypot(_r["sem_gq"], _r["sem_arr"])),
                 f"{_r['sigma']:.1f}"))
xx = np.arange(3)
for i, (lab, v, sd, sig) in enumerate(rows):
    ax.errorbar(i, v, yerr=sd, fmt="o", ms=5, color=OI["verm"], elinewidth=0.8, capsize=2)
    ax.text(i + 0.14, v, sig + " sigma", fontsize=5, color=OI["verm"],
            va="center", ha="left")
# lower bound: TRV055 Gq arm saturates, so only a bound is available
# (AngII saturates in both arms and is omitted)
_bound = abs(_A1["WT"]["TRV055"]["delta"])
ax.plot(3, -_bound, "v", ms=5, color=OI["orange"])
ax.text(3, -_bound - 0.32, f"bound >= {_bound:.1f}", ha="center", fontsize=5, color=OI["orange"])
ax.axhline(0, color="0.5", lw=0.5)
ax.axhline(-0.3, color="0.4", ls="--", lw=0.6)
ax.set_xticks(list(range(4)), ["TRV026\nWT", "TRV026\nL112A", "TRV026\nY292A", "TRV055\nWT"], fontsize=5.5)
ax.set_ylabel(r"pK$_{A,Gq}$ - pK$_{A,arr}$ (dex)")
ax.set_title("AT1R arm-versus-arm fracture")
ax.set_ylim(-2.2, 0.5)

# ---- e: muOR identity-1 heatmap (code 66) ----
ax = axs[4]
assays = ["Nb33", "mGsi", "GPA", "cAMP", "GIRK", "BarrGRK2"]
lig6 = ["Morphine", "Oxycodone", "Oliceridine", "PZM21", "SR-17018", "Buprenorphine"]
nan = np.nan
M = np.array([
    [0.03, 0.10, 0.05, 0.49, -0.78, -0.03],
    [0.19, 0.17, nan,  nan,  nan,  -0.06],
    [-0.20, -0.14, 0.40, 0.50, -0.69, -0.01],
    [-0.12, -0.11, 0.39, 0.72, -0.97, -0.05],
    [-0.26, -0.10, 0.47, 0.83, -0.83, -0.02],
    [-0.17, -0.15, 0.05, 0.56, -0.68, -0.01],
])
Mm = np.ma.masked_invalid(M)
cmap = plt.cm.RdBu_r.copy(); cmap.set_bad("0.9")
im = ax.imshow(Mm, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(6), assays, rotation=30, ha="right", fontsize=5.5)
ax.set_yticks(range(6), lig6, fontsize=5.5)
for i in range(6):
    for j in range(6):
        if not np.isnan(M[i, j]):
            ax.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=4.5,
                    color="white" if abs(M[i, j]) > 0.55 else "0.2")
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((3.5, -0.5), 1, 6, fill=False, ec=OI["verm"], lw=1.2))

cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label(r"identity-1 $\Delta$ (dex)", fontsize=5.5); cb.ax.tick_params(labelsize=5)
cb.outline.set_linewidth(0.6)
ax.set_title(r"$\mu$OR: GIRK fractured for all five ligands")
# ---- f: code 80 arm-coordinate repair ----
ax = axs[5]
d80 = pd.read_csv(os.path.join(ROOT, "results", "code80_arm_coordinate_posterior.csv"))
d80 = d80.sort_values("delta").reset_index(drop=True)
yy = np.arange(len(d80))
cols = [OI["verm"] if a == "GIRK" else (OI["blue"] if a == "cAMP" else "0.5") for a in d80["arm"]]
ax.errorbar(d80["delta"], yy, xerr=[d80["delta"] - d80["ci95_lo"], d80["ci95_hi"] - d80["delta"]],
            fmt="o", ms=4, color="0.3", elinewidth=0.6, capsize=1.5)
for i, (_, r) in enumerate(d80.iterrows()):
    ax.plot(r["delta"], i, "o", ms=5, color=cols[i])
ax.axvline(0, color="0.5", lw=0.5)
ax.set_yticks(yy, d80["arm"], fontsize=6)
ax.set_xlabel(r"arm coordinate $\delta_{arm}$ (dex)")
ax.set_title(r"arm-coordinate repair: $\Delta$logML = +128.2")
ax.text(0.98, 0.97, "dGIRK = -0.805 +/- 0.049\nGIRK |resid| 0.811 -> 0.107 dex\nLOO stable in [-0.843, -0.732]",
        transform=ax.transAxes, fontsize=4.6, va="top", ha="right", color="0.35", linespacing=1.3)
ax.invert_yaxis()

for i, ax in enumerate(axs):
    panel_label(ax, "abcdef"[i], x=-0.12, y=1.20)

fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2_fracture_maps.png"), bbox_inches="tight", dpi=300)
fig.savefig(os.path.join(HERE, "fig2_fracture_maps.pdf"), bbox_inches="tight")
print("saved fig2_fracture_maps.png / .pdf")
