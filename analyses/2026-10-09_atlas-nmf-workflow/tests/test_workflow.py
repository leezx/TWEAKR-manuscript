#!/usr/bin/env python3

from __future__ import annotations

import csv
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


class WorkflowTests(unittest.TestCase):
    def test_coverage_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            inventory = tmp / "inventory.tsv"
            legacy = tmp / "legacy.tsv"
            output = tmp / "coverage.tsv"
            write_tsv(inventory, [{
                "rds_path": "/data/A.rds", "read_status": "ok",
                "dataset_values": "Study-A",
            }])
            write_tsv(legacy, [{"dataset": "Study_A", "sample_id": "S1"}])
            subprocess.run([
                "python3", str(ROOT / "code/01_compare_legacy_coverage.py"),
                "--inventory", str(inventory), "--legacy-manifest", str(legacy),
                "--output", str(output),
            ], check=True)
            with output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            self.assertEqual(rows[0]["coverage_status"], "represented_in_legacy")

    def test_task_expansion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            prepared = tmp / "prepared" / "A"
            prepared.mkdir(parents=True)
            matrix = prepared / "S1.rds"
            matrix.touch()
            write_tsv(prepared / "prepare_manifest.row1.tsv", [{
                "dataset_id": "A", "source_id": "source_0001", "sample_id": "S1",
                "rds_path": "/data/A.rds",
                "matrix_path": str(matrix), "n_cells": 6, "n_features": 100,
                "dropped_zero_library_cells": 0, "status": "prepared", "reason": "",
            }])
            tasks = tmp / "tasks.tsv"
            combined = tmp / "combined.tsv"
            subprocess.run([
                "python3", str(ROOT / "code/04_build_nmf_tasks.py"),
                "--prepared-root", str(tmp / "prepared"), "--ranks", "5,7",
                "--output-root", str(tmp / "out"),
                "--prepared-manifest", str(combined), "--tasks", str(tasks),
            ], check=True)
            with tasks.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            self.assertEqual([row["rank"] for row in rows], ["5"])

    def test_validation_requires_every_dataset_rank(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            plan = tmp / "plan.tsv"
            tasks = tmp / "tasks.tsv"
            output = tmp / "validation.tsv"
            result_dir = tmp / "nmf" / "A" / "source_0001" / "S1" / "K5"
            result_dir.mkdir(parents=True)
            write_tsv(plan, [{
                "dataset_id": "A", "rds_path": "/data/A.rds",
                "sample_column": "sample_id", "cell_filter_column": "cell_type",
                "cell_filter_values": "malignant", "assay": "RNA",
                "enabled": "1", "review_status": "approved", "notes": "",
            }])
            write_tsv(tasks, [{
                "task_id": 1, "dataset_id": "A", "source_id": "source_0001",
                "sample_id": "S1", "matrix_path": "/tmp/S1.rds", "rank": 5,
                "output_dir": str(result_dir),
            }])
            required = [
                "fastNMF_result_object.rds", "W.matrix.rds", "H.matrix.rds",
                "deliver.cell_best_nmf.rds", "reconstruction_err.txt",
                "deliver.nmf_markers.tol0.csv", "deliver.nmf_markers.tol1.csv",
                "deliver.nmf_markers.tol2.csv",
                "deliver.nmf_top50.repeated.csv", "deliver.nmf_top50.unique.csv",
                "deliver.nmf_top100.repeated.csv", "deliver.nmf_top100.unique.csv",
                "deliver.nmf_top200.repeated.csv", "deliver.nmf_top200.unique.csv",
            ]
            for name in required:
                (result_dir / name).touch()
            write_tsv(result_dir / "status.tsv", [{"status": "complete"}])
            completed = subprocess.run([
                "python3", str(ROOT / "code/05_validate_nmf_outputs.py"),
                "--plan", str(plan), "--tasks", str(tasks), "--ranks", "5,6",
                "--output", str(output),
            ], check=False)
            self.assertEqual(completed.returncode, 1)
            with output.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle, delimiter="\t"))
            self.assertTrue(any(
                row["rank"] == "6"
                and row["validation_status"] == "dataset_rank_has_no_complete_nmf"
                for row in rows
            ))


if __name__ == "__main__":
    unittest.main()
