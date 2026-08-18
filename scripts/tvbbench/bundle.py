from __future__ import annotations

import base64
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


RUN_FIELDS = {
    "runner_experiment",
    "runner_repeat",
    "runner_run_index",
    "runner_status",
    "renderer_name",
    "total_time_min_ms",
    "total_time_median_ms",
    "total_time_max_ms",
    "total_time_avg_ms",
    "total_time_p10_ms",
    "total_time_p90_ms",
    "source_material_count",
    "active_material_bin_count",
    "material_bin_compaction_ratio",
}


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_runs(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = []
        for row in csv.DictReader(file):
            rows.append(
                {
                    key: value
                    for key, value in row.items()
                    if key in RUN_FIELDS or key.startswith("param_")
                }
            )
        return rows


def _data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/webp"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _plot_records(output_dir: Path) -> list[dict[str, Any]]:
    manifest = _read_json(output_dir / "plots" / "manifest.json", {"plots": []})
    records: list[dict[str, Any]] = []
    for plot in manifest.get("plots", []):
        png_name = next(
            (name for name in plot.get("files", []) if str(name).endswith(".png")),
            None,
        )
        png_path = output_dir / "plots" / str(png_name) if png_name else None
        records.append(
            {
                "id": plot.get("id"),
                "type": plot.get("type"),
                "status": plot.get("status"),
                "image": _data_uri(png_path) if png_path and png_path.is_file() else None,
            }
        )
    return records


def build_bundle(results_root: Path) -> dict[str, Any]:
    environment = _read_json(results_root / "environment.json", {})
    experiments: list[dict[str, Any]] = []
    for spec_path in sorted(results_root.rglob("spec.json")):
        output_dir = spec_path.parent
        spec = _read_json(spec_path, {})
        report = _read_json(output_dir / "run_report.json", {})
        artifacts = _read_json(output_dir / "artifacts.json", {})
        experiments.append(
            {
                "id": spec.get("id"),
                "title": spec.get("title"),
                "summary": spec.get("summary"),
                "tags": spec.get("tags", []),
                "fidelity": spec.get("reproduction", {}).get("fidelity"),
                "status": report.get("status"),
                "counts": {
                    "success": report.get("successful_runs", 0),
                    "salvaged": report.get("salvaged_runs", 0),
                    "failed": report.get("failed_runs", 0),
                    "skipped": report.get("skipped_runs", 0),
                },
                "artifacts": artifacts.get("rows", {}),
                "runs": _read_runs(output_dir / "runs.csv"),
                "plots": _plot_records(output_dir),
            }
        )
    return {
        "schema_version": 1,
        "kind": "tvb-performance-results",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "environment": environment,
        "experiment_count": len(experiments),
        "experiments": experiments,
    }


def export_bundle(results_root: Path, output_path: Path) -> dict[str, Any]:
    bundle = build_bundle(results_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(bundle, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    temporary.replace(output_path)
    return bundle
