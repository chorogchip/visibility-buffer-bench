from __future__ import annotations

import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from .config import EXPERIMENTS_DIR


def _load_matplotlib() -> Any:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise RuntimeError(
            "Plot dependencies are missing. Install them with "
            "'python -m pip install -r scripts/requirements.txt'."
        ) from error
    return plt


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [
            dict(row)
            for row in csv.DictReader(file)
            if row.get("runner_status") == "success"
        ]


def _number(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _sort_key(value: str) -> tuple[int, float | str]:
    number = _number(value)
    return (0, number) if number is not None else (1, value)


def _median(values: list[float]) -> float:
    return statistics.median(values) if values else math.nan


def _theme() -> dict[str, Any]:
    with (EXPERIMENTS_DIR / "plot_theme.json").open(
        "r", encoding="utf-8"
    ) as file:
        return json.load(file)


def _renderer_family(name: str) -> str:
    lower = name.lower()
    if "forward" in lower:
        return "forward"
    if "deferred" in lower:
        return "deferred"
    if "vis" in lower or "visibility" in lower:
        return "visbuf"
    return "other"


def _renderer_style(name: str, theme: dict[str, Any]) -> dict[str, Any]:
    family = _renderer_family(name)
    color = theme["renderer_families"][family]["medium"]
    lower = name.lower()
    if "prepass" in lower or "pre-pass" in lower:
        return {"color": color, "linestyle": "--", "marker": "s"}
    if "debug" in lower:
        return {"color": color, "linestyle": "-.", "marker": "^"}
    return {"color": color, "linestyle": "-", "marker": "o"}


def _canonical_pass(name: str, theme: dict[str, Any]) -> str:
    normalized = name.strip().lower().replace(" ", "_").replace("-", "_")
    return theme.get("pass_aliases", {}).get(normalized, normalized)


def _pass_color(name: str, theme: dict[str, Any], renderer: str = "") -> str:
    canonical = _canonical_pass(name, theme)
    family = _renderer_family(renderer)
    if canonical == "depth_prepass" and family in {"forward", "deferred", "visbuf"}:
        return theme["renderer_families"][family]["light"]
    if canonical == "lighting" and family in {"forward", "deferred", "visbuf"}:
        return theme["renderer_families"][family]["dark"]
    configured = theme.get("passes", {}).get(canonical)
    if configured:
        return configured["color"]
    return theme["renderer_families"]["other"]["medium"]


def _varying_parameters(rows: list[dict[str, str]]) -> list[str]:
    fields = sorted({key for row in rows for key in row if key.startswith("param_")})
    ignored = {
        "param_renderer_variant",
        "param_run_id",
        "param_run_name",
        "param_output_filepath",
        "param_auto_terminate",
    }
    return [
        field
        for field in fields
        if field not in ignored and len({row.get(field, "") for row in rows}) > 1
    ]


def _resolve_field(value: str | None, rows: list[dict[str, str]]) -> str | None:
    if value and value != "auto":
        if value.startswith("param_") or value in rows[0]:
            return value
        return f"param_{value}"
    varying = _varying_parameters(rows)
    return varying[0] if varying else None


def _save(figure: Any, output_base: Path, formats: list[str], dpi: int) -> list[str]:
    paths: list[str] = []
    for extension in formats:
        path = output_base.with_suffix(f".{extension}")
        figure.savefig(path, dpi=dpi, bbox_inches="tight")
        paths.append(path.name)
    return paths


def _plot_total(
    rows: list[dict[str, str]],
    definition: dict[str, Any],
    output_dir: Path,
    theme: dict[str, Any],
) -> list[str]:
    plt = _load_matplotlib()
    metric = str(definition.get("metric", "total_time_median_ms"))
    x_field = _resolve_field(definition.get("x"), rows)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get("renderer_name", "Unknown")].append(row)

    figure, axis = plt.subplots(figsize=tuple(theme["figure_size"]))
    if x_field is None:
        names = sorted(groups, key=lambda name: (_renderer_family(name), name))
        values = [
            _median(
                [value for row in groups[name] if (value := _number(row.get(metric))) is not None]
            )
            for name in names
        ]
        colors = [_renderer_style(name, theme)["color"] for name in names]
        axis.bar(range(len(names)), values, color=colors)
        axis.set_xticks(range(len(names)), names, rotation=20, ha="right")
    else:
        all_x_values = sorted(
            {row.get(x_field, "") for row in rows}, key=_sort_key
        )
        numeric_axis = all(_number(value) is not None for value in all_x_values)
        plotted_x: list[Any] = (
            [float(_number(value)) for value in all_x_values]
            if numeric_axis
            else all_x_values
        )
        for renderer, renderer_rows in sorted(groups.items()):
            by_x: dict[str, list[float]] = defaultdict(list)
            low_by_x: dict[str, list[float]] = defaultdict(list)
            high_by_x: dict[str, list[float]] = defaultdict(list)
            for row in renderer_rows:
                value = _number(row.get(metric))
                if value is not None:
                    by_x[row.get(x_field, "")].append(value)
                low = _number(row.get("total_time_p10_ms"))
                high = _number(row.get("total_time_p90_ms"))
                if low is not None:
                    low_by_x[row.get(x_field, "")].append(low)
                if high is not None:
                    high_by_x[row.get(x_field, "")].append(high)
            y_values = [
                _median(by_x[value]) if by_x[value] else math.nan
                for value in all_x_values
            ]
            low_values = [
                _median(low_by_x[value]) if low_by_x[value] else math.nan
                for value in all_x_values
            ]
            high_values = [
                _median(high_by_x[value]) if high_by_x[value] else math.nan
                for value in all_x_values
            ]
            style = _renderer_style(renderer, theme)
            axis.plot(
                plotted_x,
                y_values,
                label=renderer,
                linewidth=2,
                markersize=5,
                **style,
            )
            if numeric_axis and any(math.isfinite(value) for value in low_values):
                axis.fill_between(
                    plotted_x,
                    low_values,
                    high_values,
                    color=style["color"],
                    alpha=0.12,
                    linewidth=0,
                )
        axis.set_xlabel(x_field.removeprefix("param_").replace("_", " "))
        axis.legend(frameon=False)

    axis.set_ylabel(definition.get("ylabel", "GPU time (ms)"))
    axis.set_title(definition.get("title", "Median GPU time"))
    axis.set_ylim(bottom=0)
    axis.grid(axis="y", color="#D9DDE1", linewidth=0.7)
    figure.tight_layout()
    paths = _save(
        figure,
        output_dir / str(definition.get("id", "total_time")),
        list(definition.get("formats", theme["formats"])),
        int(theme["dpi"]),
    )
    plt.close(figure)
    return paths


def _plot_pass_breakdown(
    rows: list[dict[str, str]],
    definition: dict[str, Any],
    output_dir: Path,
    theme: dict[str, Any],
) -> list[str]:
    plt = _load_matplotlib()
    renderers = sorted({row.get("renderer_name", "Unknown") for row in rows})
    by_renderer_pass: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        renderer = row.get("renderer_name", "Unknown")
        measured_sum = 0.0
        for index in range(1, 32):
            name = row.get(f"pass_name_{index}", "").strip()
            value = _number(row.get(f"pass_{index}_time_avg_ms"))
            if name and value is not None and value > 0:
                measured_sum += value
                by_renderer_pass[(renderer, _canonical_pass(name, theme))].append(value)
        total = _number(row.get("pass_0_time_avg_ms"))
        if total is None:
            total = _number(row.get("total_time_avg_ms"))
        unmeasured = max(0.0, (total or 0.0) - measured_sum)
        if unmeasured > 0.00001:
            by_renderer_pass[(renderer, "other")].append(unmeasured)

    configured_order = list(theme["pass_order"])
    observed = {name for _, name in by_renderer_pass}
    pass_names = [name for name in configured_order if name in observed]
    pass_names.extend(sorted(observed - set(pass_names)))

    figure, axis = plt.subplots(figsize=tuple(theme["figure_size"]))
    bottoms = [0.0] * len(renderers)
    for pass_name in pass_names:
        values = [
            _median(by_renderer_pass[(renderer, pass_name)])
            if by_renderer_pass[(renderer, pass_name)]
            else 0.0
            for renderer in renderers
        ]
        if not any(value > 0 for value in values):
            continue
        axis.bar(
            range(len(renderers)),
            values,
            bottom=bottoms,
            label=theme.get("passes", {}).get(pass_name, {}).get("label", pass_name),
            color=[_pass_color(pass_name, theme, renderer) for renderer in renderers],
        )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    axis.set_xticks(range(len(renderers)), renderers, rotation=20, ha="right")
    axis.set_ylabel("Average GPU time (ms)")
    axis.set_title(definition.get("title", "GPU pass breakdown"))
    axis.set_ylim(bottom=0)
    axis.legend(frameon=False, ncols=2, fontsize=8)
    axis.grid(axis="y", color="#D9DDE1", linewidth=0.7)
    figure.tight_layout()
    paths = _save(
        figure,
        output_dir / str(definition.get("id", "pass_breakdown")),
        list(definition.get("formats", theme["formats"])),
        int(theme["dpi"]),
    )
    plt.close(figure)
    return paths


def _plot_scatter(
    rows: list[dict[str, str]],
    definition: dict[str, Any],
    output_dir: Path,
    theme: dict[str, Any],
) -> list[str]:
    plt = _load_matplotlib()
    x_field = _resolve_field(str(definition.get("x", "auto")), rows)
    y_field = str(definition.get("y", "total_time_median_ms"))
    if x_field is None:
        return []
    figure, axis = plt.subplots(figsize=tuple(theme["figure_size"]))
    for renderer in sorted({row.get("renderer_name", "Unknown") for row in rows}):
        points = [
            (_number(row.get(x_field)), _number(row.get(y_field)))
            for row in rows
            if row.get("renderer_name", "Unknown") == renderer
        ]
        points = [(x, y) for x, y in points if x is not None and y is not None]
        if points:
            axis.scatter(
                [point[0] for point in points],
                [point[1] for point in points],
                label=renderer,
                color=_renderer_style(renderer, theme)["color"],
                alpha=0.75,
            )
    axis.set_xlabel(x_field.removeprefix("param_").replace("_", " "))
    axis.set_ylabel(definition.get("ylabel", y_field.replace("_", " ")))
    axis.set_title(definition.get("title", "Parameter relationship"))
    axis.set_ylim(bottom=0 if bool(definition.get("zero_y", True)) else None)
    axis.legend(frameon=False)
    axis.grid(color="#D9DDE1", linewidth=0.7)
    figure.tight_layout()
    paths = _save(
        figure,
        output_dir / str(definition.get("id", "scatter")),
        list(definition.get("formats", theme["formats"])),
        int(theme["dpi"]),
    )
    plt.close(figure)
    return paths


def _plot_heatmap(
    rows: list[dict[str, str]],
    definition: dict[str, Any],
    output_dir: Path,
    theme: dict[str, Any],
) -> list[str]:
    plt = _load_matplotlib()
    try:
        import numpy as np
    except ImportError as error:
        raise RuntimeError("Heatmaps require numpy; install scripts/requirements.txt") from error

    x_field = _resolve_field(str(definition.get("x", "auto")), rows)
    y_field = _resolve_field(str(definition.get("y", "auto")), rows)
    metric = str(definition.get("metric", "total_time_median_ms"))
    if x_field is None or y_field is None or x_field == y_field:
        return []
    x_values = sorted({row.get(x_field, "") for row in rows}, key=_sort_key)
    y_values = sorted({row.get(y_field, "") for row in rows}, key=_sort_key)
    files: list[str] = []
    renderers = sorted({row.get("renderer_name", "Unknown") for row in rows})
    for renderer in renderers:
        buckets: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in rows:
            if row.get("renderer_name", "Unknown") != renderer:
                continue
            value = _number(row.get(metric))
            if value is not None:
                buckets[(row.get(x_field, ""), row.get(y_field, ""))].append(value)
        matrix = np.full((len(y_values), len(x_values)), np.nan)
        for y_index, y_value in enumerate(y_values):
            for x_index, x_value in enumerate(x_values):
                values = buckets[(x_value, y_value)]
                if values:
                    matrix[y_index, x_index] = _median(values)
        if np.isnan(matrix).all():
            continue
        figure, axis = plt.subplots(figsize=tuple(theme["figure_size"]))
        image = axis.imshow(matrix, origin="lower", aspect="auto", cmap="viridis")
        axis.set_xticks(range(len(x_values)), x_values, rotation=45, ha="right")
        axis.set_yticks(range(len(y_values)), y_values)
        axis.set_xlabel(x_field.removeprefix("param_").replace("_", " "))
        axis.set_ylabel(y_field.removeprefix("param_").replace("_", " "))
        axis.set_title(f"{definition.get('title', 'Parameter heatmap')} — {renderer}")
        figure.colorbar(image, ax=axis, label=definition.get("colorbar", "GPU time (ms)"))
        figure.tight_layout()
        safe_renderer = "".join(character.lower() if character.isalnum() else "_" for character in renderer).strip("_")
        files.extend(
            _save(
                figure,
                output_dir / f"{definition.get('id', 'heatmap')}_{safe_renderer}",
                list(definition.get("formats", theme["formats"])),
                int(theme["dpi"]),
            )
        )
        plt.close(figure)
    return files


def generate_plots(spec: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    rows = _read_rows(output_dir / "runs.csv")
    plot_dir = output_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    theme = _theme()
    definitions = spec.get("analysis", {}).get("plots", [])
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "spec_id": spec.get("id"),
        "successful_rows": len(rows),
        "plots": [],
    }
    if not rows:
        (plot_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        return manifest

    handlers = {
        "total": _plot_total,
        "line": _plot_total,
        "grouped_bar": _plot_total,
        "pass_breakdown": _plot_pass_breakdown,
        "scatter": _plot_scatter,
        "heatmap": _plot_heatmap,
    }
    for definition in definitions:
        plot_type = str(definition.get("type", "total"))
        handler = handlers.get(plot_type)
        if handler is None:
            manifest["plots"].append(
                {"id": definition.get("id"), "status": "unsupported", "type": plot_type}
            )
            continue
        files = handler(rows, definition, plot_dir, theme)
        manifest["plots"].append(
            {
                "id": definition.get("id"),
                "type": plot_type,
                "status": "generated" if files else "not_applicable",
                "files": files,
            }
        )

    (plot_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest
