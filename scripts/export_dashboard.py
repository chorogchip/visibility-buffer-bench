# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
from pathlib import Path

from tvbbench.bundle import export_bundle
from tvbbench.config import DEFAULT_OUTPUT_ROOT


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pack generated benchmark summaries and plots into one dashboard JSON."
    )
    parser.add_argument("--results", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    results_root = arguments.results.resolve()
    output = (
        arguments.output.resolve()
        if arguments.output
        else results_root / "dashboard_bundle.json"
    )
    bundle = export_bundle(results_root, output)
    print(f"Dashboard bundle: {output}")
    print(f"Experiments: {bundle['experiment_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
