#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py — reproduce the paper in manuscript order
====================================================
Runs every analysis script in the order the paper presents them, archives the
console output of each one under results/logs/, and writes results/run_manifest.json
with timings, exit codes and file hashes.

Safety rule
-----------
The archived tables in results/ were produced under pandas 1.x; re-running the
Atlas pipeline under pandas >= 2 gives a different grouping (269 vs 132 groups,
17 987 vs 10 864 pairs), which the paper documents in Section 5.5. Overwriting
those tables silently would corrupt the archive, so this runner:

  1. snapshots results/ before it starts (runs/<stamp>/before/),
  2. runs the scripts,
  3. moves any *modified* file to runs/<stamp>/regenerated/ and restores the
     archived version,
  4. keeps new files (the logs) in place.

Pass --keep to leave the regenerated files in results/ instead.

Usage
-----
    python run_all.py            # reproduce, archive logs, protect results/
    python run_all.py --keep     # keep whatever the scripts wrote
    python run_all.py --only 63,80
    python run_all.py --list
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "code")
RESULTS = os.path.join(HERE, "results")
LOGS = os.path.join(RESULTS, "logs")
RUNS = os.path.join(HERE, "runs")

# (manuscript location, script, one-line purpose)
STEPS = [
    ("§3.1", "code63_GPCR_functional_affinity_fracture.py",
     "D2R binding-versus-function fracture (Fig. 1a, Fig. 2b)"),
    ("§3.1", "code64_D2R_upstream_rate_ordering.py",
     "D2R upstream rate ordering"),
    ("§3.1", "code68_D2R_kinetic_mechanism_test.py",
     "zero-parameter kinetic occupancy model (Fig. 2c)"),
    ("§3.1", "code69_D2R_functional_state_cross_arm_map.py",
     "cross-arm pKA spread versus readout time (Fig. 2a,c)"),
    ("§3.2", "code65_AT1R_cross_arm_affinity_fracture.py",
     "AT1R arm separation with binding in between (Fig. 1b, Fig. 2d)"),
    ("§3.3", "code66_MOR_Gillis_internal_consistency.py",
     "μOR cell-level identity violation map (Fig. 1c, Fig. 2e)"),
    ("§3.3", "code80_Gillis_arm_coordinate_extended_model.py",
     "μOR one-coordinate-per-arm extension, M1 versus M0 (Fig. 1c, Fig. 2f)"),
    ("§3.4", "code67_BiasedSignalingAtlas_meta_audit.py",
     "Atlas meta-audit, pair deviations and Emax census"),
    ("§3.4", "code71_Atlas_full_identity_pipeline.py",
     "Atlas identity pipeline, entry/group/paper tables (Table 1, Fig. 1d)"),
    ("§3.5", "code73_robustness_triplet_blind_jackknife.py",
     "common-mode error, conservative aggregation, column jackknife (Fig. 3f)"),
    ("§3.6", "code77_Atlas_constraint_projection_fracture_probability.py",
     "constraint projection and mixture-model fracture probability (Fig. 3c,d)"),
    ("§4", "code72_audit_method_false_positive_selfcheck.py",
     "false-positive rate, detection power, controls (Table 2)"),
    ("§4", "code72b_null_at_fixed_cut.py",
     "independent-error null at fixed cuts, entry and pair level (§3.4 text)"),
    ("SI §2", "code47_P5_blind_adjudication_boundary_predictor.py",
     "P5 blind adjudication, Keshelava 2018"),
    ("SI §2", "code47b_P5_erratum_readjudication.py",
     "P5 erratum re-adjudication after timing exclusions"),
]

SKIP = {".git", "__pycache__", "runs"}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(root: str) -> dict[str, str]:
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in filenames:
            p = os.path.join(dirpath, name)
            out[os.path.relpath(p, root)] = sha256(p)
    return out


def _run_artefact(rel: str) -> bool:
    """Files this runner owns: always rewritten by a run, never restored."""
    rel = rel.replace("\\", "/")
    return rel.startswith("logs/") or rel == "run_manifest.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", action="store_true",
                    help="leave regenerated files in results/ instead of restoring the archive")
    ap.add_argument("--only", default="", help="comma-separated script numbers, e.g. 63,80")
    ap.add_argument("--list", action="store_true", help="list the steps and exit")
    args = ap.parse_args()

    if args.list:
        for i, (where, script, what) in enumerate(STEPS, 1):
            print(f"{i:2d}  {where:7s} {script:62s} {what}")
        return 0

    steps = STEPS
    if args.only:
        keys = {s.strip() for s in args.only.split(",") if s.strip()}
        steps = [s for s in steps if any(s[1].startswith("code" + k) for k in keys)]
        if not steps:
            print("no step matched --only", args.only)
            return 2

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(RUNS, stamp)
    before_dir = os.path.join(run_dir, "before")
    regen_dir = os.path.join(run_dir, "regenerated")
    os.makedirs(LOGS, exist_ok=True)
    os.makedirs(before_dir, exist_ok=True)

    print("=" * 88)
    print("run_all — paper order reproduction")
    print("=" * 88)
    print(f"python  : {sys.version.split()[0]}  ({platform.platform()})")
    for mod in ("numpy", "scipy", "pandas", "matplotlib", "openpyxl"):
        try:
            m = __import__(mod)
            print(f"{mod:11s}: {getattr(m, '__version__', '?')}")
        except Exception as exc:  # noqa: BLE001
            print(f"{mod:11s}: not importable ({exc})")
    print()

    before = snapshot(RESULTS)
    for rel, digest in before.items():
        dst = os.path.join(before_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(RESULTS, rel), dst)
    print(f"snapshot of results/ taken: {len(before)} files -> {os.path.relpath(before_dir, HERE)}\n")

    header = f"{'#':>2}  {'where':7s} {'script':58s} {'exit':>4} {'secs':>6}"
    print(header)
    print("-" * len(header))

    records = []
    for i, (where, script, what) in enumerate(steps, 1):
        path = os.path.join(CODE, script)
        if not os.path.exists(path):
            print(f"{i:2d}  {where:7s} {script:58s} {'--':>4} {'--':>6}  MISSING")
            records.append({"order": i, "section": where, "script": script,
                            "status": "missing", "exit": None, "seconds": None})
            continue
        t0 = time.time()
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        proc = subprocess.run([sys.executable, path], cwd=CODE,
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env)
        secs = time.time() - t0
        log_path = os.path.join(LOGS, script.replace(".py", ".log"))
        with open(log_path, "w", encoding="utf-8") as fh:
            fh.write(f"$ {sys.executable} code/{script}\n")
            fh.write(f"# exit {proc.returncode}  {secs:.1f}s  "
                     f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n")
            fh.write(proc.stdout)
            if proc.stderr:
                fh.write("\n--- stderr ---\n" + proc.stderr)
        print(f"{i:2d}  {where:7s} {script:58s} {proc.returncode:4d} {secs:6.1f}")
        records.append({"order": i, "section": where, "script": script, "purpose": what,
                        "status": "ok" if proc.returncode == 0 else "failed",
                        "exit": proc.returncode, "seconds": round(secs, 2),
                        "log": os.path.relpath(log_path, HERE).replace("\\", "/"),
                        "log_sha256": sha256(log_path)})

    after = snapshot(RESULTS)
    modified = sorted(k for k in before
                      if k in after and before[k] != after[k] and not _run_artefact(k))
    new = sorted(k for k in after if k not in before)
    gone = sorted(k for k in before if k not in after and not _run_artefact(k))

    if modified:
        os.makedirs(regen_dir, exist_ok=True)
        for rel in modified:
            dst = os.path.join(regen_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(RESULTS, rel), dst)
        if not args.keep:
            for rel in modified:
                shutil.copy2(os.path.join(before_dir, rel), os.path.join(RESULTS, rel))
    for rel in gone:
        shutil.copy2(os.path.join(before_dir, rel), os.path.join(RESULTS, rel))

    failed = [r for r in records if r["status"] != "ok"]
    packages = {}
    for mod in ("numpy", "scipy", "pandas", "matplotlib", "openpyxl"):
        try:
            packages[mod] = getattr(__import__(mod), "__version__", "?")
        except Exception:  # noqa: BLE001
            packages[mod] = "not importable"
    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "steps": records,
        "results_changed": modified,
        "results_new": new,
        "results_restored": [] if args.keep else modified,
        "failed": [r["script"] for r in failed],
    }
    with open(os.path.join(RESULTS, "run_manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    print()
    print("-" * 88)
    print(f"steps      : {len(records)}  (failed: {len(failed)})")
    print(f"new files  : {len(new)}  (logs and manifest stay in results/)")
    print(f"modified   : {len(modified)}")
    if modified:
        for rel in modified:
            print(f"   {rel}  ->  runs/{stamp}/regenerated/{rel}")
        if args.keep:
            print("   --keep: regenerated files left in results/")
        else:
            print("   archived versions restored in results/ (pass --keep to keep the new ones)")
    print(f"manifest   : results/run_manifest.json")
    print("=" * 88)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
