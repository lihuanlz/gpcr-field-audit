# The quantitative currency of GPCR bias signalling fails its own algebraic identities

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23402860.svg)](https://doi.org/10.5281/zenodo.23402860)

Companion code, results and manuscript source for the paper:

> H. Li. *The quantitative currency of GPCR bias signalling fails its own algebraic identities.* Companion manuscript (2026), split from the umbrella project [cell-communication-audit](https://github.com/lihuanlz/cell-communication-audit) (archived at Zenodo, doi:10.5281/zenodo.23008824).

## Layout

- `manuscript/` — LaTeX source, compiled PDF, figure PNGs, figure-generation scripts.
- `code/` — analysis scripts (ours): P5 blind adjudication and erratum re-adjudication (code47/47b), functional-affinity fracture (code63), D2R upstream rate ordering (code64), AT1R cross-arm fracture (code65), MOR internal consistency (code66), BiasedSignalingAtlas meta-audit (code67), D2R kinetic mechanism (code68) and functional-state map (code69), Atlas full-identity pipeline (code71), false-positive self-check (code72), robustness triplet (code73), constraint projection (code77), Gillis arm-coordinate extended model (code80).
- `results/` — derived outputs (ours): P5 adjudication tables and verdict JSONs, Atlas violation tables, MOR residuals.
- `data_external/keshelava2018/` — Supplementary Data 3 of Keshelava et al. (2018), per-cell Fura-2 peaks; see `data_external/PROVENANCE.md`.

## Running

Python 3 (numpy/scipy/matplotlib/pandas). Scripts run against `data_external/` and the archived tables in `results/`.

## Ownership

Code, derived results and manuscript: the author's work product (MIT for code, CC BY 4.0 for text). Third-party data are mirrored only where small and license-clear (PROVENANCE.md); large source archives (BiasedSignalingAtlas exports, Gillies 2020 supplements) are referenced, not re-hosted.

## Companion papers

- *The p53 pulse encoder counts by topological necessity* → [p53-pulse-encoder](https://github.com/lihuanlz/p53-pulse-encoder)
- *Amplitude and midpoint statistics of the same chemotaxis cells demand incompatible receptor models* → [chemotaxis-receptor-layer](https://github.com/lihuanlz/chemotaxis-receptor-layer)
- *The price of absolute scale* (framework) → [scale-free-framework](https://github.com/lihuanlz/scale-free-framework)
