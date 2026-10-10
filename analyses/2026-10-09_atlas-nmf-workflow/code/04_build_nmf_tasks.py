#!/usr/bin/env python3
"""Combine preparation manifests and expand successful matrices across ranks."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepared-root", type=Path, required=True)
    parser.add_argument("--ranks", required=True, help="Comma-separated ranks")
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--prepared-manifest", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, required=True)
    args = parser.parse_args()

    ranks = sorted({int(value) for value in args.ranks.split(",") if value.strip()})
    if not ranks or min(ranks) < 2:
        raise ValueError("At least one rank >= 2 is required")

    manifests = sorted(args.prepared_root.glob("**/prepare_manifest.row*.tsv"))
    if not manifests:
        raise FileNotFoundError(f"No preparation manifests under {args.prepared_root}")

    prepared_rows: list[dict[str, str]] = []
    for manifest in manifests:
        prepared_rows.extend(read_tsv(manifest))

    args.prepared_manifest.parent.mkdir(parents=True, exist_ok=True)
    fields = list(prepared_rows[0])
    with args.prepared_manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(prepared_rows)

    task_rows: list[dict[str, str | int]] = []
    for row in prepared_rows:
        if row["status"] != "prepared":
            continue
        for rank in ranks:
            if rank > int(row["n_cells"]):
                continue
            output_dir = (
                args.output_root / "nmf" / row["dataset_id"] / row["source_id"]
                / row["sample_id"] / f"K{rank}"
            )
            task_rows.append({
                "task_id": len(task_rows) + 1,
                "dataset_id": row["dataset_id"],
                "source_id": row["source_id"],
                "sample_id": row["sample_id"],
                "matrix_path": row["matrix_path"],
                "rank": rank,
                "output_dir": str(output_dir),
            })

    if not task_rows:
        raise RuntimeError("No eligible NMF tasks were generated")
    args.tasks.parent.mkdir(parents=True, exist_ok=True)
    with args.tasks.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(task_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(task_rows)
    print(f"Prepared rows: {len(prepared_rows)}")
    print(f"NMF tasks: {len(task_rows)}")
    print(f"Wrote: {args.tasks}")


if __name__ == "__main__":
    main()
