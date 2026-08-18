from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import EXPERIMENTS_DIR
from .specs import (
    CANONICAL_META_KEYS,
    SpecError,
    all_argument_keys,
    parameter_sets,
    program_argument_names,
    read_json,
    run_count,
)


def verify_spec(path: Path) -> dict[str, Any]:
    spec = read_json(path)
    errors: list[str] = []
    warnings: list[str] = []

    if spec.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    spec_id = spec.get("id")
    if not isinstance(spec_id, str) or not spec_id:
        errors.append("id must be a non-empty string")
    if not isinstance(spec.get("title"), str) or not spec["title"].strip():
        errors.append("title must be a non-empty string")
    if spec.get("executable") != "@executable/release":
        warnings.append("portfolio measurements should use @executable/release")

    unknown_top = sorted(set(spec) - CANONICAL_META_KEYS)
    if unknown_top:
        errors.append("unknown top-level keys: " + ", ".join(unknown_top))

    argument_names = program_argument_names()
    unknown_arguments = sorted(all_argument_keys(spec) - argument_names)
    if unknown_arguments:
        errors.append("unknown ProgramArgument keys: " + ", ".join(unknown_arguments))

    try:
        combinations = list(parameter_sets(spec))
    except SpecError as error:
        errors.append(str(error))
        combinations = []

    for index, combination in enumerate(combinations):
        variant = combination.get("renderer_variant")
        try:
            valid_variant = 1 <= int(variant) <= 15
        except (TypeError, ValueError):
            valid_variant = False
        if not valid_variant:
            errors.append(f"parameter set {index} has invalid renderer_variant={variant!r}")
            break
        for key in ("scene_path", "camera_filepath"):
            value = combination.get(key)
            if isinstance(value, str) and Path(value).is_absolute():
                errors.append(f"parameter set {index} contains absolute {key}")
                break

    analysis = spec.get("analysis")
    if not isinstance(analysis, dict) or not isinstance(analysis.get("plots"), list):
        errors.append("analysis.plots must be an array")

    reproduction = spec.get("reproduction", {})
    fidelity = reproduction.get("fidelity") if isinstance(reproduction, dict) else None
    if fidelity not in {"exact", "adapted"}:
        errors.append("reproduction.fidelity must be exact or adapted")

    return {
        "path": str(path),
        "id": spec_id,
        "run_count": run_count(spec) if combinations else 0,
        "fidelity": fidelity,
        "errors": errors,
        "warnings": warnings,
    }


def verify_specs(paths: list[Path]) -> dict[str, Any]:
    reports = [verify_spec(path) for path in paths]
    ids = [report["id"] for report in reports if report["id"]]
    duplicate_ids = sorted({spec_id for spec_id in ids if ids.count(spec_id) > 1})
    if duplicate_ids:
        reports[0]["errors"].append("duplicate spec ids: " + ", ".join(duplicate_ids))
    return {
        "schema_version": 1,
        "spec_count": len(reports),
        "run_count": sum(report["run_count"] for report in reports),
        "exact_count": sum(report["fidelity"] == "exact" for report in reports),
        "adapted_count": sum(report["fidelity"] == "adapted" for report in reports),
        "error_count": sum(len(report["errors"]) for report in reports),
        "warning_count": sum(len(report["warnings"]) for report in reports),
        "specs": reports,
    }


def canonical_spec_paths() -> list[Path]:
    return sorted((EXPERIMENTS_DIR / "specs").rglob("*.json"))
