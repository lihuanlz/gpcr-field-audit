# The quantitative currency of GPCR bias signalling fails its own algebraic identities

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23402860.svg)](https://doi.org/10.5281/zenodo.23402860)

Companion code, results and manuscript source for the paper:

> H. Li. *The quantitative currency of GPCR bias signalling fails its own algebraic identities.* Companion manuscript (2026), split from the umbrella project [cell-communication-audit](https://github.com/lihuanlz/cell-communication-audit) (archived at Zenodo, doi:10.5281/zenodo.23008824).

## Layout

- `manuscript/` — LaTeX source, compiled PDF, figure PNGs, figure-generation scripts.
- `code/` — analysis scripts (ours): P5 blind adjudication and erratum re-adjudication (code47/47b), functional-affinity fracture (code63), D2R upstream rate ordering (code64), AT1R cross-arm fracture (code65), MOR internal consistency (code66), BiasedSignalingAtlas meta-audit (code67), D2R kinetic mechanism (code68) and functional-state map (code69), Atlas full-identity pipeline (code71), false-positive self-check (code72), fixed-cut null (code72b), robustness triplet (code73), constraint projection (code77), Gillis arm-coordinate extended model (code80).
- `results/` — derived outputs (ours): P5 adjudication tables and verdict JSONs, Atlas violation and audit tables, MOR and arm-coordinate tables.
- `public_data/` — the three third-party input sets the scripts read: the Biased Signaling Atlas export, the Klein Herenbrink 2016 D2R workbook, and the Keshelava 2018 raw traces. See `data_external/PROVENANCE.md`.

## Running

Python 3 with numpy, scipy, pandas, openpyxl and matplotlib; the exact versions used to produce the archived results are pinned in `requirements.txt`. Every script builds its paths relative to the repository; there are no absolute paths left.

- On Windows, set `PYTHONIOENCODING=utf-8` first: several scripts write Greek letters and mathematical symbols to stdout.
- `results/atlas_audit/` holds the Atlas tables quoted in the paper: 269 assay groups, 17,987 pair comparisons, 3,931 triplets. They now re-derive exactly under the pinned versions. The composite group key is built with an explicit missing-value rule because pandas 1.x and pandas 2+ disagree about whether a missing component stringifies or propagates; without that rule the same input collapses to 132 groups and 10,864 pairs.
- All fifteen scripts were re-run from a clean copy on 2026-10-19 and every one exits 0. `python run_all.py --check` compares each regenerated table with its archived copy: 11 identical, 10 known P5 differences, 0 unexpected. The code80 model comparison, the P5 adjudications and the MOR residuals reproduce to machine precision; P5 cell counts follow the numeric build, but its verdicts do not.

## Ownership

Code, derived results and manuscript: the author's work product (MIT for code, CC BY 4.0 for text). Third-party inputs are re-hosted in `public_data/` where the analysis cannot run without them (Atlas export, D2R workbook, Keshelava traces); the Gillis 2020 supplement is transcribed inside the scripts and is not re-hosted. See `data_external/PROVENANCE.md`.

## Companion papers

- *The p53 pulse encoder counts by topological necessity* → [p53-pulse-encoder](https://github.com/lihuanlz/p53-pulse-encoder)
- *Amplitude and midpoint statistics of the same chemotaxis cells demand incompatible receptor models* → [chemotaxis-receptor-layer](https://github.com/lihuanlz/chemotaxis-receptor-layer)
- *The price of absolute scale* (framework) → [scale-free-framework](https://github.com/lihuanlz/scale-free-framework)
