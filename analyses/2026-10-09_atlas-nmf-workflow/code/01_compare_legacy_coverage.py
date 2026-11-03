#!/usr/bin/env python3
"""Compare dataset representation in new Seurat inventory and legacy NMF."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path


def normalized_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip() and not item.startswith("...+")]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def select_column(rows: list[dict[str, str]], choices: tuple[str, ...]) -> str:
    if not rows:
        raise ValueError("Input table is empty")
    for choice in choices:
        if choice in rows[0]:
            return choice
    raise ValueError(f"None of the required columns are present: {choices}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--legacy-manifest", type=Path, required=True)
    parser.add_argument("--aliases", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    inventory = read_tsv(args.inventory)
    legacy = read_tsv(args.legacy_manifest)
    legacy_dataset_col = select_column(legacy, ("dataset_id", "dataset", "study", "study_id"))
    legacy_sample_col = select_column(legacy, ("sample_id", "sample", "rds_path", "outfile"))

    aliases: dict[str, str] = {}
    if args.aliases:
        for row in read_tsv(args.aliases):
            aliases[normalized_id(row["alias"])] = row["dataset_id"]

    new_files: dict[str, set[str]] = defaultdict(set)
    raw_names: dict[str, set[str]] = defaultdict(set)
    unresolved_files: list[str] = []
    for row in inventory:
        values = split_values(row.get("dataset_values", ""))
        if row.get("read_status") != "ok" or len(values) != 1:
            unresolved_files.append(row.get("rds_path", ""))
            continue
        raw = values[0]
        key = normalized_id(raw)
        canonical = aliases.get(key, raw)
        canonical_key = normalized_id(canonical)
        new_files[canonical_key].add(row["rds_path"])
        raw_names[canonical_key].add(raw)

    legacy_samples: dict[str, set[str]] = defaultdict(set)
    legacy_names: dict[str, set[str]] = defaultdict(set)
    for row in legacy:
        raw = row[legacy_dataset_col].strip()
        if not raw:
            continue
        key = normalized_id(aliases.get(normalized_id(raw), raw))
        legacy_samples[key].add(row[legacy_sample_col])
        legacy_names[key].add(raw)

    keys = sorted(set(new_files) | set(legacy_samples))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "dataset_key", "new_dataset_names", "new_rds_count",
            "legacy_dataset_names", "legacy_sample_count", "coverage_status",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for key in keys:
            if key in new_files and key in legacy_samples:
                status = "represented_in_legacy"
            elif key in new_files:
                status = "not_represented_in_legacy"
            else:
                status = "legacy_only"
            writer.writerow({
                "dataset_key": key,
                "new_dataset_names": "|".join(sorted(raw_names[key])),
                "new_rds_count": len(new_files[key]),
                "legacy_dataset_names": "|".join(sorted(legacy_names[key])),
                "legacy_sample_count": len(legacy_samples[key]),
                "coverage_status": status,
            })

    if unresolved_files:
        unresolved = args.output.with_suffix(".unresolved.tsv")
        with unresolved.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, delimiter="\t")
            writer.writerow(["rds_path", "reason"])
            for path in unresolved_files:
                writer.writerow([path, "read_error_or_nonunique_dataset_id"])
        print(f"WARNING: {len(unresolved_files)} unresolved RDS files -> {unresolved}")
    print(f"Wrote coverage audit: {args.output}")


if __name__ == "__main__":
    main()
