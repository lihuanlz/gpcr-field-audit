# Third-party data provenance

## Shipped here

| Folder | Source | Terms |
|---|---|---|
| `keshelava2018/peak_values.csv` | Keshelava et al., *Nat. Commun.* 9, 876 (2018), Supplementary Data 3 (PMC5830429): per-cell Fura-2 ratio peaks, 27 experiments × 433 cells × 7 ACh doses × 5 repetitions, baseline-subtracted by the authors' pipeline | Open-access article supplementary (CC BY 4.0). Cite the original paper. Mirrored here on behalf of the companion repository [scale-free-framework](https://github.com/lihuanlz/scale-free-framework), whose `cascade_audit_gpcr_ca.py` consumes it; no script in this repo reads this file. Note: the authors' MATLAB script carries a legacy dose ladder; the companion analysis follows the Methods ladder. |

## Referenced but not re-hosted

| Source | Used for | Access |
|---|---|---|
| BiasedSignalingAtlas (biasedsignalingatlas.org) | community coupling/efficacy tables for code67/71/77 | Project website / associated publications |
| Gillis et al., *Sci. Signal.* 13, eaaz3140 (2020), main Tables 1–3 and SI Table S1 | μOR ligand series for code66/80 | Publisher supplementary (~98 MB, not mirrored) |
| Klein Herenbrink et al., *Nat. Commun.* 7, 10842 (2016) | D2R anchor case | Publisher site |
| Wingler et al., *Science* 367, 888–892 (2020) | AT1R anchor case | Publisher site |

All verdicts in `results/` are our own derived work product.
