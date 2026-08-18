# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from tvbbench import runner
from tvbbench.config import (
    DEFAULT_OUTPUT_ROOT,
    ROOT,
    expand_spec,
    load_config,
    run_build,
)
from tvbbench.normalize import normalize_results
from tvbbench.plot import generate_plots
from tvbbench.specs import (
    load_suite,
    read_json,
    resolve_suite_specs,
    run_count,
)
from tvbbench.verify import canonical_spec_paths, verify_specs


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _git(*arguments: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *arguments],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


def _gpu_info() -> list[dict[str, str]]:
    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return []
    result = []
    for line in output.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 3:
            result.append(
                {"name": parts[0], "driver_version": parts[1], "memory_mib": parts[2]}
            )
    return result


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _environment(executable: Path | None) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "captured_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "python": sys.version,
        "processor": platform.processor(),
        "gpu": _gpu_info(),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain")),
        "executable": str(executable) if executable else None,
        "executable_sha256": _sha256(executable) if executable else None,
    }


def _safe_reset_output(path: Path, output_root: Path) -> None:
    resolved = path.resolve()
    root = output_root.resolve()
    if resolved == root or root not in resolved.parents:
        raise ValueError(f"Refusing to remove output outside {root}: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def _finalize_report(
    report: dict[str, Any], report_json: Path, status: str
) -> None:
    finished = runner.now_iso()
    report["status"] = status
    report["finished_at"] = finished
    report["last_updated_at"] = finished
    runner.safe_write_json(report_json, report)


def _run_one(
    spec_path: Path,
    config: dict[str, Any],
    output_root: Path,
    overwrite: bool,
    no_plots: bool,
) -> int:
    canonical = read_json(spec_path)
    expanded = expand_spec(canonical, config)
    spec_id = str(canonical["id"])
    output_dir = output_root / Path(spec_id)
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(
                f"Output already exists: {output_dir}. Use --overwrite to replace it."
            )
        _safe_reset_output(output_dir, output_root)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_csv = output_dir / "raw.csv"
    spec_copy = output_dir / "spec.json"
    resolved_copy = output_dir / "resolved_spec.json"
    report_json = output_dir / "run_report.json"
    shutil.copy2(spec_path, spec_copy)
    _write_json(resolved_copy, expanded)

    report = runner.initial_report(spec_path, spec_copy, raw_csv, report_json)
    report.update(
        {
            "status": "running",
            "spec_id": spec_id,
            "resolved_spec": str(resolved_copy),
            "last_updated_at": runner.now_iso(),
        }
    )
    runner.safe_write_json(report_json, report)

    try:
        exit_code = runner.run_experiment(
            spec_path,
            expanded,
            output_dir,
            raw_csv,
            report_json,
            report,
        )
        status = (
            "completed_with_errors"
            if exit_code
            else "completed_with_skips"
            if report.get("skipped_runs", 0)
            else "completed"
        )
        _finalize_report(report, report_json, status)
    except KeyboardInterrupt:
        _finalize_report(report, report_json, "interrupted")
        raise
    except Exception as error:
        exit_code = runner.handle_fatal_error(
            error, spec_path, spec_copy, raw_csv, report
        )
        _finalize_report(report, report_json, "fatal_error")

    counts = normalize_results(output_dir, raw_csv)
    plots = None if no_plots else generate_plots(canonical, output_dir)
    _write_json(
        output_dir / "artifacts.json",
        {"schema_version": 1, "spec_id": spec_id, "rows": counts, "plots": plots},
    )
    runner.print_summary(raw_csv, spec_copy, report_json, report)
    return exit_code


def _analyze_one(spec_path: Path, output_root: Path, no_plots: bool) -> None:
    canonical = read_json(spec_path)
    output_dir = output_root / Path(str(canonical["id"]))
    raw_csv = output_dir / "raw.csv"
    if not raw_csv.is_file():
        raise FileNotFoundError(f"Missing raw result CSV: {raw_csv}")
    counts = normalize_results(output_dir, raw_csv)
    plots = None if no_plots else generate_plots(canonical, output_dir)
    _write_json(
        output_dir / "artifacts.json",
        {"schema_version": 1, "spec_id": canonical["id"], "rows": counts, "plots": plots},
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build, run, normalize, and plot reproducible TVBPerf experiments."
    )
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--suite", default="smoke", help="Suite name or JSON path.")
    selection.add_argument(
        "--spec", action="append", help="Canonical experiment JSON path; repeatable."
    )
    parser.add_argument("--config", type=Path, help="Machine-local config JSON.")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--configuration", choices=("Release", "Debug"), default="Release")
    parser.add_argument("--build", action="store_true", help="Configure/build before running.")
    parser.add_argument("--verify", action="store_true", help="Validate canonical specs and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve and count runs only.")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--keep-going", action="store_true")
    return parser


def main() -> int:
    arguments = _parser().parse_args()
    output_root = arguments.output_root.resolve()

    if arguments.verify:
        paths = canonical_spec_paths()
        report = verify_specs(paths)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if report["error_count"] else 0

    if arguments.spec:
        spec_paths = [(ROOT / path).resolve() for path in arguments.spec]
        suite_name = "explicit"
    else:
        suite_path, suite = load_suite(arguments.suite)
        spec_paths = resolve_suite_specs(suite_path, suite)
        suite_name = str(suite.get("id", suite_path.stem))

    verification = verify_specs(spec_paths)
    if verification["error_count"]:
        print(json.dumps(verification, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    total_runs = sum(run_count(read_json(path)) for path in spec_paths)
    print(f"Suite: {suite_name}")
    print(f"Specs: {len(spec_paths)}")
    print(f"Runs: {total_runs}")
    print(f"Output: {output_root}")
    if arguments.dry_run:
        for path in spec_paths:
            spec = read_json(path)
            print(f"  {spec['id']}: {run_count(spec)} run(s)")
        return 0

    config = load_config(arguments.config)
    if arguments.build:
        run_build(config, arguments.configuration)

    expanded_first = expand_spec(read_json(spec_paths[0]), config)
    executable_value = expanded_first.get("executable")
    executable = Path(str(executable_value)) if executable_value else None
    output_root.mkdir(parents=True, exist_ok=True)
    _write_json(output_root / "environment.json", _environment(executable))

    failures = 0
    for index, spec_path in enumerate(spec_paths, start=1):
        print(f"\n[{index}/{len(spec_paths)}] {spec_path.name}")
        try:
            if arguments.analyze_only:
                _analyze_one(spec_path, output_root, arguments.no_plots)
                exit_code = 0
            else:
                exit_code = _run_one(
                    spec_path,
                    config,
                    output_root,
                    arguments.overwrite,
                    arguments.no_plots,
                )
            failures += int(exit_code != 0)
        except KeyboardInterrupt:
            return 130
        except Exception:
            failures += 1
            traceback.print_exc()
        if failures and not arguments.keep_going:
            break

    print(f"\nCompleted: {len(spec_paths) - failures}, failed: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
