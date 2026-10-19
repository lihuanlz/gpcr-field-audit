# Third-party data provenance

## Shipped here

| Folder | Source | Terms |
|---|---|---|
| `public_data/BiasedSignalingAtlas/Biased_ligand_single_pathway_data.xlsx` | Biased Signaling Atlas export (biasedsignalingatlas.org), `Data` sheet, 9,041 rows × 38 columns. Consumed by `code67` and `code71`; `code73`, `code77` and `code72` read the derived tables in `results/atlas_audit/`. | Community database, downloaded verbatim from the public site; re-hosted here so the Atlas pipeline runs end to end. Cite the Atlas and its associated publications. |
| `public_data/D2R_KleinHerenbrink2016/SupplementaryData1.xlsx` | Klein Herenbrink et al., *Nat. Commun.* 7, 10842 (2016), Supplementary Data 1. Consumed by `code64`; `code63`, `code68` and `code69` transcribe the relevant columns inline. | Publisher supplementary data; re-hosted for reproducibility of the D2R anchor case. Cite the original paper. |
| `public_data/Keshelava2018/SD1/source_data_1/` | Keshelava et al., *Nat. Commun.* 9, 876 (2018), Supplementary Data 1: raw per-experiment traces (27 `.dot` files with their `.config` files). Consumed by `code47` and `code47b`. | Open-access article supplementary (CC BY 4.0). Cite the original paper. |
| `data_external/keshelava2018/peak_values.csv` | Keshelava et al., *Nat. Commun.* 9, 876 (2018), Supplementary Data 3 (PMC5830429): per-cell Fura-2 ratio peaks, 27 experiments × 433 cells × 7 ACh doses × 5 repetitions, baseline-subtracted by the authors' pipeline. | Open-access article supplementary (CC BY 4.0). Mirrored on behalf of the companion repository [scale-free-framework](https://github.com/lihuanlz/scale-free-framework); no script in this repo reads this file. Note: the authors' MATLAB script carries a legacy dose ladder; the companion analysis follows the Methods ladder. |

## Referenced but not re-hosted

| Source | Used for | Access |
|---|---|---|
| Gillis et al., *Sci. Signal.* 13, eaaz3140 (2020), main Tables 1–3 and SI Table S1 | μOR ligand series for `code66` and `code80` | Publisher supplementary (~98 MB). The values used are transcribed inside the scripts and were checked value-by-value against the PDFs; no input file is read at run time. |
| Wingler et al., *Science* 367, 888–892 (2020) | AT1R anchor case for `code65` | Publisher site. Values are transcribed inside the script. |

## Notes

- All verdicts in `results/` are our own derived work product.
- `results/atlas_audit/` holds the intermediate tables of the pandas-1.x run reported in the paper (269 groups, 17,987 pair comparisons, 3,931 triplets). Re-running `code71` under pandas ≥ 2 gives a different grouping (132 groups, 10,864 pairs, 3,167 triplets); the paper reports both in Section 5.5 and uses the 1.x numbers throughout.
- `code72b_null_at_fixed_cut.py` needs no input file: it regenerates the null distribution from the same seed as `code72`.
