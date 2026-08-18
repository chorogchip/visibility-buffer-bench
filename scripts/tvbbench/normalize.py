from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


RUN_CONTEXT_FIELDS = (
    "runner_experiment",
    "runner_repeat",
    "runner_run_index",
    "runner_status",
    "renderer_name",
    "param_renderer_variant",
    "total_time_median_ms",
    "total_time_p10_ms",
    "total_time_p90_ms",
)


def _read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file() or path.stat().st_size == 0:
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def _write_rows(
    path: Path, fieldnames: list[str], rows: list[dict[str, Any]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_results(output_dir: Path, raw_csv: Path) -> dict[str, int]:
    fields, rows = _read_rows(raw_csv)
    _write_rows(output_dir / "runs.csv", fields, rows)

    pass_rows: list[dict[str, Any]] = []
    for row in rows:
        context = {name: row.get(name, "") for name in RUN_CONTEXT_FIELDS}
        for key, value in row.items():
            if key.startswith("param_"):
                context[key] = value
        for pass_index in range(32):
            name = row.get(f"pass_name_{pass_index}", "").strip()
            timing = row.get(f"pass_{pass_index}_time_avg_ms", "").strip()
            if not name or not timing:
                continue
            try:
                numeric_timing = float(timing)
            except ValueError:
                continue
            pass_rows.append(
                {
                    **context,
                    "pass_index": pass_index,
                    "pass_name": name,
                    "pass_time_avg_ms": numeric_timing,
                }
            )

    pass_fields = list(RUN_CONTEXT_FIELDS) + sorted(
        {key for row in pass_rows for key in row if key.startswith("param_")}
    ) + ["pass_index", "pass_name", "pass_time_avg_ms"]
    _write_rows(output_dir / "passes.csv", pass_fields, pass_rows)

    excluded = {raw_csv.resolve(), (output_dir / "runs.csv").resolve(), (output_dir / "passes.csv").resolve()}
    frame_sources = [
        path
        for path in output_dir.rglob("*.csv")
        if path.resolve() not in excluded and "result" in path.stem.lower()
    ]
    frame_fields = ["source_file"]
    frame_rows: list[dict[str, str]] = []
    for source in sorted(frame_sources):
        source_fields, source_rows = _read_rows(source)
        for field in source_fields:
            if field not in frame_fields:
                frame_fields.append(field)
        for row in source_rows:
            frame_rows.append(
                {"source_file": str(source.relative_to(output_dir)), **row}
            )
    _write_rows(output_dir / "frames.csv", frame_fields, frame_rows)

    return {
        "runs": len(rows),
        "passes": len(pass_rows),
        "frames": len(frame_rows),
    }
