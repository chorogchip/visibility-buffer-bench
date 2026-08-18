from __future__ import annotations

import json
import os
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS_DIR = ROOT / "experiments"
DEFAULT_OUTPUT_ROOT = ROOT / "results"


class ConfigError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ConfigError(f"Configuration root must be an object: {path}")
    return value


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: Path | None = None) -> dict[str, Any]:
    example = _read_json(EXPERIMENTS_DIR / "local.example.json")
    local_path = path or EXPERIMENTS_DIR / "local.json"
    if local_path.exists():
        example = _merge(example, _read_json(local_path))
    example["_config_path"] = str(local_path)
    return example


def _resolve_config_path(value: str) -> Path:
    path = Path(os.path.expandvars(value)).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def find_executable(configuration: str) -> Path | None:
    config = configuration.lower()
    executable_dir = "Release" if config == "release" else "Debug"
    candidates = list(
        (ROOT / "out" / "build").glob(
            f"*/bin/{executable_dir}/TVBPerf.exe"
        )
    )
    candidates.extend(
        (ROOT / "out" / "build").glob("*/bin/TVBPerf.exe")
    )
    candidates = [path.resolve() for path in candidates if path.is_file()]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def resolve_executable(config: dict[str, Any], name: str) -> Path:
    configured = str(config.get("executables", {}).get(name, "auto"))
    if configured.lower() == "auto":
        found = find_executable(name)
        if found is None:
            raise ConfigError(
                f"No {name} TVBPerf.exe was found under out/build. "
                "Run with --build or set experiments/local.json."
            )
        return found
    return _resolve_config_path(configured)


def resolve_alias(value: Any, config: dict[str, Any]) -> Any:
    if not isinstance(value, str) or not value.startswith("@"):
        return value

    try:
        namespace, name = value[1:].split("/", 1)
    except ValueError as error:
        raise ConfigError(f"Invalid path alias: {value}") from error

    if namespace == "executable":
        return str(resolve_executable(config, name))
    if namespace == "camera":
        path = EXPERIMENTS_DIR / "camera_paths" / f"{name}.csv"
        if not path.is_file():
            raise ConfigError(f"Unknown camera alias: {value}")
        return str(path.resolve())
    if namespace == "scene":
        configured = config.get("scenes", {}).get(name)
        if configured:
            return str(_resolve_config_path(str(configured)))
        return str((EXPERIMENTS_DIR / "missing_scenes" / name).resolve())
    raise ConfigError(f"Unknown alias namespace: {value}")


def _expand_value(value: Any, config: dict[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: _expand_value(item, config) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_value(item, config) for item in value]
    return resolve_alias(value, config)


def expand_spec(spec: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    expanded = deepcopy(spec)
    for key in ("executable", "base", "sweep", "samples"):
        if key in expanded:
            expanded[key] = _expand_value(expanded[key], config)
    return expanded


def _find_vcvars64() -> Path | None:
    configured = os.environ.get("VSINSTALLDIR")
    if configured:
        candidate = Path(configured) / "VC/Auxiliary/Build/vcvars64.bat"
        if candidate.is_file():
            return candidate

    roots = (
        Path(r"C:\Program Files\Microsoft Visual Studio"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio"),
    )
    matches: list[Path] = []
    for root in roots:
        if root.exists():
            matches.extend(root.glob("*/*/VC/Auxiliary/Build/vcvars64.bat"))
    return sorted(matches, reverse=True)[0] if matches else None


def run_build(config: dict[str, Any], configuration: str) -> None:
    build_settings = config.get("build", {})
    configured_dir = str(
        build_settings.get(
            "directory", f"out/build/reproduce-{configuration}"
        )
    ).replace("{configuration}", configuration)
    build_dir = _resolve_config_path(configured_dir)
    generator = str(build_settings.get("generator", "Ninja"))

    commands: list[list[str]] = []
    if not (build_dir / "CMakeCache.txt").is_file():
        commands.append(
            [
                "cmake",
                "-S",
                str(ROOT),
                "-B",
                str(build_dir),
                "-G",
                generator,
                f"-DCMAKE_BUILD_TYPE={configuration}",
            ]
        )
    commands.append(
        ["cmake", "--build", str(build_dir), "--config", configuration]
    )

    vcvars = _find_vcvars64()
    for command in commands:
        if os.name == "nt" and vcvars is not None:
            rendered = subprocess.list2cmdline(command)
            subprocess.run(
                f'call "{vcvars}" >nul && {rendered}',
                cwd=ROOT,
                check=True,
                shell=True,
            )
        else:
            subprocess.run(command, cwd=ROOT, check=True)

    executable = build_dir / "bin" / configuration / "TVBPerf.exe"
    if not executable.is_file():
        executable = build_dir / "bin" / "TVBPerf.exe"
    config.setdefault("executables", {})[configuration.lower()] = str(executable)


def ensure_plot_dependencies() -> None:
    if shutil.which("python") is None:
        raise ConfigError("Python is not available on PATH.")
