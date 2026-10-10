#!/usr/bin/env python3
"""Validate all sample/rank outputs and enforce approved dataset coverage."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--ranks", required=True, help="Comma-separated approved ranks")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected_ranks = {value.strip() for value in args.ranks.split(",") if value.strip()}
    if not expected_ranks:
        raise ValueError("At least one expected rank is required")

    approved = {
        row["dataset_id"]
        for row in read_tsv(args.plan)
        if row.get("enabled") == "1" and row.get("review_status") == "approved"
    }
    if not approved:
        raise RuntimeError("No approved datasets in plan")

    tasks = read_tsv(args.tasks)
    completed_by_dataset: dict[str, int] = defaultdict(int)
    completed_by_dataset_rank: dict[tuple[str, str], int] = defaultdict(int)
    report: list[dict[str, str | int]] = []
    for task in tasks:
        out = Path(task["output_dir"])
        required = [
            "status.tsv", "fastNMF_result_object.rds", "W.matrix.rds", "H.matrix.rds",
            "deliver.cell_best_nmf.rds", "reconstruction_err.txt",
            "deliver.nmf_markers.tol0.csv", "deliver.nmf_markers.tol1.csv",
            "deliver.nmf_markers.tol2.csv",
            "deliver.nmf_top50.repeated.csv", "deliver.nmf_top50.unique.csv",
            "deliver.nmf_top100.repeated.csv", "deliver.nmf_top100.unique.csv",
            "deliver.nmf_top200.repeated.csv", "deliver.nmf_top200.unique.csv",
        ]
        missing = [name for name in required if not (out / name).is_file()]
        status = "complete" if not missing else "incomplete"
        if status == "complete":
            status_rows = read_tsv(out / "status.tsv")
            if len(status_rows) != 1 or status_rows[0].get("status") != "complete":
                status = "invalid_status"
        if status == "complete":
            completed_by_dataset[task["dataset_id"]] += 1
            completed_by_dataset_rank[(task["dataset_id"], task["rank"])] += 1
        report.append({
            **task,
            "validation_status": status,
            "missing_files": "|".join(missing),
        })

    for dataset in sorted(approved):
        if completed_by_dataset[dataset] == 0:
            report.append({
                "task_id": "",
                "dataset_id": dataset,
                "source_id": "",
                "sample_id": "",
                "matrix_path": "",
                "rank": "",
                "output_dir": "",
                "validation_status": "dataset_has_no_complete_nmf",
                "missing_files": "",
            })
        for rank in sorted(expected_ranks, key=int):
            if completed_by_dataset_rank[(dataset, rank)] == 0:
                report.append({
                    "task_id": "",
                    "dataset_id": dataset,
                    "source_id": "",
                    "sample_id": "",
                    "matrix_path": "",
                    "rank": rank,
                    "output_dir": "",
                    "validation_status": "dataset_rank_has_no_complete_nmf",
                    "missing_files": "",
                })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "task_id", "dataset_id", "source_id", "sample_id", "matrix_path", "rank",
        "output_dir", "validation_status", "missing_files",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(report)

    failures = [row for row in report if row["validation_status"] != "complete"]
    print(f"Validated tasks: {len(tasks)}")
    print(f"Approved datasets: {len(approved)}")
    print(f"Failures: {len(failures)}")
    print(f"Wrote: {args.output}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
