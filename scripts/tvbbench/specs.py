from __future__ import annotations

import itertools
import glob
import json
import re
from pathlib import Path
from typing import Any, Iterator

from .config import EXPERIMENTS_DIR, ROOT


class SpecError(ValueError):
    pass


CANONICAL_META_KEYS = {
    "$schema",
    "schema_version",
    "id",
    "title",
    "summary",
    "tags",
    "reproduction",
    "analysis",
    "executable",
    "repeat",
    "timeout_seconds",
    "keep_individual_csv",
    "base",
    "sweep",
    "samples",
}


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise SpecError(f"JSON root must be an object: {path}")
    return value


def load_suite(name_or_path: str) -> tuple[Path, dict[str, Any]]:
    path = Path(name_or_path)
    if path.suffix.lower() != ".json":
        path = EXPERIMENTS_DIR / "suites" / f"{name_or_path}.json"
    elif not path.is_absolute():
        path = (ROOT / path).resolve()
    if not path.is_file():
        raise SpecError(f"Suite does not exist: {path}")
    suite = read_json(path)
    if not isinstance(suite.get("specs"), list) or not suite["specs"]:
        raise SpecError(f"Suite must contain a non-empty 'specs' array: {path}")
    return path, suite


def resolve_suite_specs(suite_path: Path, suite: dict[str, Any]) -> list[Path]:
    result: list[Path] = []
    for raw in suite["specs"]:
        path = Path(str(raw))
        candidate = path if path.is_absolute() else suite_path.parent / path
        rendered = str(candidate)
        if any(character in rendered for character in "*?["):
            matches = [Path(item).resolve() for item in glob.glob(rendered, recursive=True)]
            if not matches:
                raise SpecError(f"Suite pattern matched no specs: {raw}")
            result.extend(path for path in matches if path.is_file())
            continue
        path = candidate.resolve()
        if not path.is_file():
            raise SpecError(f"Suite references a missing spec: {path}")
        result.append(path)
    return list(dict.fromkeys(sorted(result)))


def normalize_keys(values: dict[str, Any]) -> dict[str, Any]:
    return {
        normalized: value
        for key, value in values.items()
        if not (normalized := str(key).replace("-", "_")).startswith("_")
    }


def parameter_sets(spec: dict[str, Any]) -> Iterator[dict[str, Any]]:
    base = normalize_keys(spec.get("base", {}))
    sweep = normalize_keys(spec.get("sweep", {}))
    samples = spec.get("samples")
    if samples is not None and sweep:
        raise SpecError("A spec cannot use both 'sweep' and 'samples'.")
    if samples is not None:
        if not isinstance(samples, list) or not samples:
            raise SpecError("'samples' must be a non-empty array.")
        for sample in samples:
            if not isinstance(sample, dict):
                raise SpecError("Every sample must be an object.")
            yield {**base, **normalize_keys(sample)}
        return
    if sweep:
        names = list(sweep)
        values: list[list[Any]] = []
        for name in names:
            choices = sweep[name]
            if not isinstance(choices, list) or not choices:
                raise SpecError(f"Sweep '{name}' must be a non-empty array.")
            values.append(choices)
        for combination in itertools.product(*values):
            yield {**base, **dict(zip(names, combination))}
        return
    yield base


def run_count(spec: dict[str, Any]) -> int:
    return sum(1 for _ in parameter_sets(spec)) * int(spec.get("repeat", 1))


def program_argument_names() -> set[str]:
    header = (ROOT / "include" / "ProgramArgument.h").read_text(
        encoding="utf-8-sig"
    )
    macro = header.split("#define ProgramArgument_MAC", 1)[1].split(
        "#define ProgramResult_MAC", 1
    )[0]
    return {
        match.group(1)
        for match in re.finditer(
            r"X\([^,]+,\s*([A-Za-z_][A-Za-z0-9_]*)\s*,", macro
        )
    }


def all_argument_keys(spec: dict[str, Any]) -> set[str]:
    keys = set(normalize_keys(spec.get("base", {})))
    keys.update(normalize_keys(spec.get("sweep", {})))
    for sample in spec.get("samples", []):
        if isinstance(sample, dict):
            keys.update(normalize_keys(sample))
    return keys
