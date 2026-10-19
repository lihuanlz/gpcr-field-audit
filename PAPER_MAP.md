# Paper map — manuscript location to script to archived output

The scripts are numbered by the order in which they were written, not by the order in
which the paper presents them. This file is the translation table. The numbering is part
of the manuscript (`Methods`: "codes 63–80"), so it is kept as is.

## Reproduce everything

```bash
set PYTHONIOENCODING=utf-8          # Windows: the scripts print Greek letters
python run_all.py                   # manuscript order, one command
python run_all.py --list            # show the order without running
python run_all.py --only 63,80      # a subset
```

`run_all.py` does three things beyond calling the scripts:

1. archives every script's console output under `results/logs/<script>.log`, because most
   of these scripts compute numbers and print them rather than writing files;
2. writes `results/run_manifest.json` — python and package versions, per-step exit code and
   wall time, SHA-256 of each log;
3. protects the archive. `results/` is snapshotted first; any file the run modifies is copied
   to `runs/<stamp>/regenerated/` and the archived version is put back, so a re-run cannot
   silently replace the tables the paper quotes. `--keep` leaves the new files in place.

## Map

| Manuscript | Item | Script | Output |
|---|---|---|---|
| §3.1 D2R | Fig. 1a, Fig. 2b | `code63` | `results/logs/code63_*.log` |
| §3.1 D2R | Fig. 2c (kinetic drift) | `code68` | `results/logs/code68_*.log` |
| §3.1 D2R | Fig. 2a, Fig. 2c (cross-arm spread) | `code69` | `results/logs/code69_*.log` |
| §3.1 D2R | upstream rate ordering | `code64` | `results/logs/code64_*.log` |
| §3.2 AT1R | Fig. 1b, Fig. 2d | `code65` | `results/logs/code65_*.log` |
| §3.3 μOR | Fig. 1c left, Fig. 2e | `code66` | `results/logs/code66_*.log` |
| §3.3 μOR | Fig. 1c right, Fig. 2f, Table 1 | `code80` | `results/code80_*.csv` (5 files) |
| §3.4 Atlas | Table 1, Fig. 1d | `code67` | `results/logs/code67_*.log`; `results/atlas_pair_violations.csv` with `--write` |
| §3.4 Atlas | Table 1 (group, paper and Emax census) | `code71` | `results/atlas_audit/atlas_audit_{entries,groups,papers}.csv`, `atlas_audit_summary.json` |
| §3.5 robustness | Fig. 3f | `code73` | `results/atlas_audit/atlas_confidence_matrix.csv` |
| §3.6 repair | Fig. 3c,d | `code77` | `results/atlas_audit/atlas_repair_projection.csv`, `atlas_fracture_probability.csv` |
| §4 calibration | Table 2 | `code72` | `results/logs/code72_*.log` |
| §3.4 (null) | fixed-cut independent-error null | `code72b` | `results/logs/code72b_*.log` |
| SI §2 P5 | P5 tables and verdicts | `code47`, `code47b` | `results/Keshelava2018_P5*/` |

## Things worth knowing before you run anything

**The Atlas grouping was a code defect, now fixed.** The assay-group key is a string
concatenation; under pandas 1.x a missing component became the text `nan`, while pandas 2+
propagate the missing value so the whole key turns missing and `groupby` drops the row. That
silently halved the corpus (269 groups and 17,987 pairs became 132 and 10,864). `code67/71/73/77`
now pin the 1.x rule explicitly, and the archived tables re-derive exactly under the pinned
versions. If you write your own grouping over the Atlas, do the same or your numbers will
differ for reasons that have nothing to do with the data.

**Most numbers live in console output, not in files.** Only `code47/47b`, `code71`, `code77`
and `code80` write tables. The rest print. That is why the logs are archived by `run_all.py`.

**The P5 experiment admission is environment-sensitive.** `code47` admits experiments by a
chain-validation step built on peak detection. The archived tables came from the 2026-08-16
run, which admitted 11 experiments and 208 cells (195 after the erratum exclusions). Under the
pinned versions in `requirements.txt` the same data and the same code admit 12 experiments and
233 cells (218 after the erratum): three of the 27 borderline experiments cross the threshold.
Unit AUCs move by at most 0.03 (robust arms 0.13 and 0.23) and every adjudication clause
reproduces verbatim — P5-1/P5-2 intermediate before the erratum, P5-1 falsified after it. The
count is not reproducible; the verdict is.

`run_all.py --check` reports the Atlas and P5 files as *known environment differences* and
fails only on an unexpected one, so "does it still reproduce?" is a command, not an opinion.

**`code67 --write` is the only producer of `results/atlas_pair_violations.csv`.** The archived
copy is the pandas-1.x run; the export reflects whichever environment you run it in and adds
the signed deviation (`dev_signed`), which the archived copy does not carry.

**The two P5 scripts are not part of the manuscript.** `code47`/`code47b` adjudicate a boundary
predictor on the Keshelava 2018 calcium dataset — a different receptor system from the GPCR
audit. They were removed from the Supporting Information in v1.0.8 and now sit under the
`archive` label in `run_all.py`; their outputs stay under `results/` for the record. Nothing in
the paper depends on them, and their cell counts follow the numeric build (208 vs 233), which is
why `--check` treats them as the one known environment difference.

**Verdict file names match the archive.** `code47`/`code47b` write `code47_verdict.json` and
`code47b_verdict.json`, the same names the archived copies carry.

**The anchor figures read their numbers from `results/derived/`.** `code63` writes
`code63_d2r.json` (per ligand, per pathway: functional pK_A, pK_i, Δ and σ) and `code65` writes
`code65_at1r.json` (per condition: both arm affinities, binding, Δ and σ). `make_fig1.py` and
`make_fig2.py` load those files, so the panels cannot drift from the analysis again — which is
exactly how the AT1R error survived: the figure had its own copy of the numbers. Re-run
`code63`/`code65` before regenerating the figures. The remaining panels (the D2R time courses in
Fig. 2a–c, the μOR heat map in Fig. 2e, and the calibration bars in Fig. 3e–f) still carry their
values inline; those numbers have been checked against their sources and have not drifted, but
they are not yet data-bound.
