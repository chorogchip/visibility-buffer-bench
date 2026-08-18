from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tvbbench.bundle import build_bundle  # noqa: E402
from tvbbench.config import expand_spec, load_config  # noqa: E402
from tvbbench.normalize import normalize_results  # noqa: E402
from tvbbench.verify import canonical_spec_paths, verify_specs  # noqa: E402


class ExperimentInventoryTests(unittest.TestCase):
    def test_canonical_inventory_matches_migration_audit(self) -> None:
        report = verify_specs(canonical_spec_paths())
        self.assertEqual(report["spec_count"], 66)
        self.assertEqual(report["run_count"], 4280)
        self.assertEqual(report["exact_count"], 57)
        self.assertEqual(report["adapted_count"], 9)
        self.assertEqual(report["error_count"], 0)
        self.assertEqual(report["warning_count"], 0)

    def test_portable_aliases_expand_without_machine_paths_in_specs(self) -> None:
        config = load_config(ROOT / "experiments" / "local.example.json")
        expanded = expand_spec(
            {
                "executable": "@executable/release",
                "base": {
                    "camera_filepath": "@camera/standard_camera",
                    "scene_path": "@scene/sponza",
                },
            },
            {
                **config,
                "executables": {"release": str(ROOT / "fake" / "TVBPerf.exe")},
            },
        )
        self.assertTrue(expanded["base"]["camera_filepath"].endswith("standard_camera.csv"))
        self.assertIn("missing_scenes", expanded["base"]["scene_path"])

    def test_plot_theme_keeps_renderer_and_pass_semantics(self) -> None:
        theme = json.loads((ROOT / "experiments" / "plot_theme.json").read_text())
        families = theme["renderer_families"]
        self.assertEqual(families["forward"]["medium"], "#3D8FC4")
        self.assertEqual(families["deferred"]["medium"], "#E69F00")
        self.assertEqual(families["visbuf"]["medium"], "#2FA77D")
        self.assertEqual(theme["passes"]["visibility"]["color"], families["visbuf"]["light"])
        self.assertEqual(theme["passes"]["resolve"]["color"], families["visbuf"]["dark"])


class ResultPipelineTests(unittest.TestCase):
    def test_normalized_result_becomes_one_dashboard_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory)
            output = results / "synthetic" / "smoke"
            plots = output / "plots"
            plots.mkdir(parents=True)

            raw = output / "raw.csv"
            fields = [
                "runner_experiment",
                "runner_repeat",
                "runner_run_index",
                "runner_status",
                "renderer_name",
                "param_renderer_variant",
                "total_time_median_ms",
                "total_time_p10_ms",
                "total_time_p90_ms",
                "pass_name_0",
                "pass_0_time_avg_ms",
            ]
            with raw.open("w", encoding="utf-8-sig", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerow(
                    {
                        "runner_experiment": "synthetic/smoke",
                        "runner_repeat": "0",
                        "runner_run_index": "0",
                        "runner_status": "success",
                        "renderer_name": "VisBuf",
                        "param_renderer_variant": "4",
                        "total_time_median_ms": "1.25",
                        "total_time_p10_ms": "1.20",
                        "total_time_p90_ms": "1.30",
                        "pass_name_0": "total",
                        "pass_0_time_avg_ms": "1.25",
                    }
                )

            counts = normalize_results(output, raw)
            self.assertEqual(counts, {"runs": 1, "passes": 1, "frames": 0})

            (results / "environment.json").write_text(
                json.dumps({"gpu": [{"name": "test GPU"}]}), encoding="utf-8"
            )
            (output / "spec.json").write_text(
                json.dumps(
                    {
                        "id": "synthetic/smoke",
                        "title": "Smoke",
                        "summary": "Bundle contract",
                        "tags": ["synthetic"],
                        "reproduction": {"fidelity": "exact"},
                    }
                ),
                encoding="utf-8",
            )
            (output / "run_report.json").write_text(
                json.dumps(
                    {
                        "status": "completed",
                        "successful_runs": 1,
                        "salvaged_runs": 0,
                        "failed_runs": 0,
                        "skipped_runs": 0,
                    }
                ),
                encoding="utf-8",
            )
            (output / "artifacts.json").write_text(
                json.dumps({"rows": counts}), encoding="utf-8"
            )
            (plots / "total.png").write_bytes(b"not-a-real-png-but-portable")
            (plots / "manifest.json").write_text(
                json.dumps(
                    {
                        "plots": [
                            {
                                "id": "total",
                                "type": "total",
                                "status": "generated",
                                "files": ["total.png"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            bundle = build_bundle(results)
            self.assertEqual(bundle["kind"], "tvb-performance-results")
            self.assertEqual(bundle["experiment_count"], 1)
            experiment = bundle["experiments"][0]
            self.assertEqual(experiment["counts"]["success"], 1)
            self.assertEqual(experiment["runs"][0]["renderer_name"], "VisBuf")
            self.assertTrue(experiment["plots"][0]["image"].startswith("data:image/png;base64,"))


if __name__ == "__main__":
    unittest.main()
