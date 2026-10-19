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
| Gillis et al., *Sci. Signal.* 13, eaaz3140 (2020), main Tables 1–3 and SI Table S1 | μOR ligand series for `code66` and `code80` | Publisher supplementary. Values are transcribed inside the scripts; no input file is read at run time. Verified cell by cell on 2026-10-19 (see below). |
| Wingler et al., *Science* 367, 888–892 (2020), main text and SI Tables S4/S5 | AT1R anchor case for `code65` | Publisher site. Values are transcribed inside the script. Verified cell by cell on 2026-10-19, after which eight cells were corrected (see below). |

## Transcription audit (2026-10-19)

Four source sets were checked cell by cell against the PDFs, rendering each table with `pdftoppm`
and reading it at 2× rather than trusting a text extraction — text extraction reorders table
columns, which is exactly how the AT1R error arose.

| Source | Compared with | Result |
|---|---|---|
| Gillis 2020, main Tables 1–3 (Emax, pEC50, log τ) and SI Table S1 (log τ/K_A) | `code66` | 4 tables, all cells match. GIRK is the untreated column (DAMGO = 100), which is what identity 1 requires. |
| Wingler 2020, SI Table S4 (binding log K_i) | `code65` | 5 ligands, all match. |
| Wingler 2020, SI Table S5 (Emax / log EC50) | `code65` | **8 cells wrong**, corrected. The arrestin block is ordered *Wild-type (5% DNA) · L112A · Wild-type · Y292A*; the 5%-DNA column is an expression-matched control for L112A, not the wild-type response, and TRV026 had the Emax of one column blended with the pEC50 of another. Corrected Δ pK_A: WT −2.05 → −1.52 dex (5.0σ → 3.8σ), L112A −1.53 → −1.19 (3.8σ), Y292A −0.61 → −0.48 (1.2σ), TRV055 bound 1.6 → 0.8 dex. |
| Klein Herenbrink 2016, SI Table S2 (Δlog τ/K_A), Table S5 (pK_i) and Table S6 (PPHT pK_a) | `code63` | pK_i 7/7 exact, PPHT pK_a 7/7 exact, 40 pathway differences match within 0.01 dex (rounding). |
| BiasedSignalingAtlas export | `code67`, `code71` | Shipped file is byte-identical to the archived copy (SHA-256 `5d087379…`). |

Archived copies used for the check (SHA-256 prefixes): Wingler SI `7cf0c273…`, Gillis SI
`0150ba54…`, Gillis main text `b621f223…`, Klein Herenbrink SI `53be7387…`, and the two shipped
spreadsheets `76988cc2…` (D2R) and `5d087379…` (Atlas), both of which match the archive byte for
byte.

## Notes

- All verdicts in `results/` are our own derived work product.
- The Atlas pipeline pins the pandas-1.x missing-value behaviour in the composite group key, so the archived tables (269 groups, 17,987 pairs, 3,931 triplets) re-derive exactly under the pinned environment. Without that pin, pandas 2+ collapses the same input to 132 groups and 10,864 pairs; the paper reports that collapse in Section 5.5 as what an unpinned re-run would produce.
- `code72b_null_at_fixed_cut.py` needs no input file: it regenerates the null distribution from the same seed as `code72`.
