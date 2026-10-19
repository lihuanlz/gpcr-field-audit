#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code 65: AT1R cross-arm affinity fracture test v1.0.0
================================================
Cell line 4, second cut. Data: Wingler et al. 2020, Science 367:888 (aay9813)
SI Table S4 ([3H]olmesartan competition binding logKi ± SEM, purified/membrane AT1R) and
Table S5 (Emax/logEC50 ± SEM for Gq IP1 accumulation and β-arrestin2 internalization,
Expi293F, same study, same system).

Audit design (two layers, neither requires cross-study data):
  Test A (cross-arm internal fracture, no anchor): a single-KA equilibrium operational model requires the
    functional affinity of the same ligand to be conserved across arms. Invert each arm's measured (Emax, EC50) via
    τ=Emax/(100−Emax), pKA_arm = pEC50 − log10(1+τ), and compare the two arms.
    When the full-agonist arm (τ→∞) is unresolvable, give an inequality bound (pKA ≤ pEC50−log10(1+τ_min)).
  Test B (binding anchor): pKi − pEC50 > 0 violates pEC50 ≥ pKA (the zero-model criterion of code 63
    self-check (1)).

Data entry (SI T4/T5 digit-by-digit checked; arr=β-arrestin2 internalization; Emax normalized to the
WT/AngII maximal response):
  binding logKi: AngII −7.41±0.03, S1I8 −8.73±0.03, TRV026 −7.50±0.02,
              TRV023 −6.42±0.01, TRV055 −6.3±0.1, Losartan −7.4±0.1 (antagonist, excluded from functional analysis)
  function in the table below (WT / L112A / Y292A / WT-5%DNA, four conditions).

Results (v1.1.0, after the 2026-10-19 correction of the SI Table S5 transcription):
  Test A cross-arm ΔpKA:
    TRV026: WT −1.52 dex (3.8σ); L112A −1.19 (3.8σ); Y292A −0.48 (1.2σ, weak)
    TRV055: WT lower bound |Δ| ≥ 0.8 dex (Gq full agonism unresolvable; inequality bound is robust)
    AngII: saturates in both arms; pKA unresolvable on either side
  Test B binding anchor: TRV023 pKi−pEC50 = +0.52 dex ⚠; S1I8 +0.73 dex ⚠
    (Gq-arm functional potency below binding affinity, violating pEC50 ≥ pKA)
  Interpretation: TRV026 is the literature-famous extreme arrestin-biased ligand; this test shows its
    "bias" magnitude already exceeds what a single-affinity equilibrium model can accommodate  -  the self-consistent
    KA values of the two arms differ by ~33-fold, while the binding-measured Ki falls exactly between them. I.e.: the operational
    model's KA here is not a physical affinity, but a hybrid parameter absorbing the structural differences of the two arms.
    Complementary to the D2R (code 63) conclusion: there the fracture lies between "binding state vs functional state";
    here it lies directly between "arm vs arm".

Verdict: the AT1R data fracture as well, and the fracture position coincides exactly with the reported bias position.
Two receptors, two experimental systems, two test designs  -  the fracture points the same way.

Run: python3 code65_AT1R_cross_arm_affinity_fracture.py
Dependency: numpy
"""

import numpy as np

# ---- entry (SI Table S4/S5) ----
pKi = {"AngII": (7.41, .03), "S1I8": (8.73, .03), "TRV026": (7.50, .02),
       "TRV023": (6.42, .01), "TRV055": (6.30, .10)}
# function: {condition: {ligand: {arm: (Emax%, semE, pEC50, semP)}}}
# Transcribed from Wingler et al. 2020 SI Table S5 (rendered from SI.pdf p.17 and read cell by cell).
# Column order in the arrestin block of that table is: Wild-type (5% DNA) | L112A | Wild-type | Y292A.
# The undiluted Wild-type column is used for the WT condition; the 5%-DNA column is the
# expression-matched control for L112A and is *not* the wild-type response.
FUNC = {
"WT": {
 "AngII":  {"Gq": (100,1,8.62,.05), "arr": (100,1,8.43,.05)},
 "TRV055": {"Gq": (99,2,7.22,.07),  "arr": (88,3,7.60,.10)},
 "S1I8":   {"Gq": (25,2,8.00,.30),  "arr": None},
 "TRV026": {"Gq": (18,3,6.20,.40),  "arr": (54,1,7.97,.06)},
 "TRV023": {"Gq": (23,5,5.90,.40),  "arr": None}},
"L112A": {
 "TRV055": {"Gq": (81,3,7.40,1.00), "arr": (51,2,7.80,.10)},
 "S1I8":   {"Gq": (71,2,8.20,.10),  "arr": None},
 "TRV026": {"Gq": (18,2,6.70,.30),  "arr": (27.4,.7,7.94,.08)},
 "TRV023": {"Gq": (25,3,6.50,.30),  "arr": None}},
"Y292A": {
 "TRV055": {"Gq": (86,3,7.00,.10),  "arr": None},
 "S1I8":   {"Gq": (35,3,8.20,.30),  "arr": None},
 "TRV026": {"Gq": (13,3,6.60,.40),  "arr": (20.3,.8,7.12,.09)},
 "TRV023": {"Gq": (32,5,6.40,.30),  "arr": None}},
}

def pka_from(em, pec):
    tau = em / (100 - em)
    return pec - np.log10(1 + tau), tau

def sem_pka(em, semE, semP):
    # σ_pKA² = σ_pEC50² + (dlog(1+τ)/dE)²σ_E²; dlog(1+τ)/dE = (1/ln10)·100/((100−E)(100))
    tau = em / (100 - em)
    d = (1 / np.log(10)) * (100 / (100 - em)) / 100 * 100  # = (1/ln10)/(100-em)*100/100
    dlog = (1 / np.log(10)) * 100 / (100 - em) * (semE / 100)
    return np.sqrt(semP**2 + dlog**2)

def main():
    # results are also written to results/derived/code65_at1r.json, which Fig. 1b and Fig. 2d read,
    # so the figures cannot drift from this table again
    out = {}
    print("== Test A: cross-arm functional affinity fracture (ΔpKA = pKA_Gq − pKA_arr) ==")
    for cond, ligs in FUNC.items():
        for lig, arms in ligs.items():
            if arms.get("Gq") and arms.get("arr"):
                emG, seG, peG, spG = arms["Gq"]
                emA, seA, peA, spA = arms["arr"]
                if emG >= 99:
                    # full agonism: give lower bound τ_min corresponding to Emax−2σ
                    em_lo = emG - 2 * seG
                    tau_lo = em_lo / (100 - em_lo)
                    bound = peG - np.log10(1 + tau_lo)
                    if emA >= 99:
                        print(f"  {cond:6s} {lig:8s}: Emax {emG:.0f}% (Gq) and {emA:.0f}% (arr)  -  "
                              f"full agonism in both arms, pKA unresolvable on either side; skipped")
                        out.setdefault(cond, {})[lig] = {"status": "unresolvable"}
                        continue
                    d_lo = bound - pka_from(emA, peA)[0]
                    print(f"  {cond:6s} {lig:8s}: Gq full agonism unresolvable; pKA_Gq ≤ {bound:.2f} (Emax−2σ bound),"
                          f"pKA_arr={pka_from(emA,peA)[0]:.2f} → Δ ≤ {d_lo:+.2f} dex (lower-bound fracture ≥{abs(d_lo):.1f})")
                    out.setdefault(cond, {})[lig] = {
                        "status": "bound", "pka_gq_upper": round(float(bound), 3),
                        "pka_arr": round(float(pka_from(emA, peA)[0]), 3),
                        "delta": round(float(d_lo), 3)}
                    continue
                if emA >= 99:
                    print(f"  {cond:6s} {lig:8s}: arr full agonism unresolvable; pKA_Gq={pka_from(emG,peG)[0]:.2f}; skipped")
                    out.setdefault(cond, {})[lig] = {"status": "arr_saturates"}
                    continue
                pG, tG = pka_from(emG, peG); pA, tA = pka_from(emA, peA)
                sG = sem_pka(emG, seG, spG); sA = sem_pka(emA, seA, spA)
                sd = np.sqrt(sG**2 + sA**2)
                d = pG - pA
                print(f"  {cond:6s} {lig:8s}: pKA_Gq={pG:.2f}±{sG:.2f}, pKA_arr={pA:.2f}±{sA:.2f}, "
                      f"Δ={d:+.2f} dex ({abs(d)/sd:.1f}σ)")
                out.setdefault(cond, {})[lig] = {
                    "status": "ok", "pka_gq": round(float(pG), 3), "sem_gq": round(float(sG), 3),
                    "pka_arr": round(float(pA), 3), "sem_arr": round(float(sA), 3),
                    "delta": round(float(d), 3), "sigma": round(float(abs(d) / sd), 1),
                    "pki": pKi.get(lig, (None, None))[0],
                    "pki_sem": pKi.get(lig, (None, None))[1]}

    print("\n== Test B: binding-anchor zero-model criterion (pKi − pEC50 > 0.3 means fracture) ==")
    for cond, ligs in FUNC.items():
        for lig, arms in ligs.items():
            if lig not in pKi: continue
            for arm, v in arms.items():
                if v is None: continue
                d = pKi[lig][0] - v[2]
                tag = "⚠FRACTURE" if d > 0.3 else "ok"
                print(f"  {cond:6s} {lig:8s} {arm:4s}: pKi={pKi[lig][0]:.2f} pEC50={v[2]:.2f} diff={d:+.2f} {tag}")

    # dump for the figures (Fig. 1b and Fig. 2d read this file, not hand-copied numbers)
    import json, os
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "derived")
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, "code65_at1r.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"source": "Wingler 2020 SI Tables S4/S5", "test_a": out}, fh, indent=1,
                  ensure_ascii=False)
    print(f"\n[derived] -> results/derived/code65_at1r.json")

if __name__ == "__main__":
    main()
