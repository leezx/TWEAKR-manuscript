#!/usr/bin/env python3
"""Extract the authors' own reference tables from Supplementary Table 1 (MOESM1).

Everything downstream depends on using the *paper's* definitions rather than ours,
so that the question "is TWEAKR an oncofetal marker" is answered on their terms
and cannot be dismissed as a signature-definition artefact.

Writes to the HotData processed/ tree, not to the repository: these are verbatim
copies of a 44 MB published supplementary workbook, and the repo keeps only the
statistics computed from them.

Usage:  python3 -I 00_extract_supplementary.py <MOESM1.xlsx> <outdir>

Sheets taken:
  S1c  DE genes, neoplastic metacluster vs rest  -> is Tnfrsf12a an OnF marker, by
       the authors' own differential expression
  S1d  mouse OnF / Stem signatures               -> scoring in the A and AKSP models
  S1f  human OnF / Stem signatures               -> cross-species check
  S1g  lineage-specific (Lukonin) signatures     -> the Fig. 1j-l lineage plasticity score
  S2c  YAP / FOS knockdown during initiation     -> GSE263047 has no processed counts,
       so the authors' DESeq2 output is the only route to that contrast
  S2d  DN-FOS during initiation
  S2e  YAP(S6A) +/- FOS during initiation
  S3i  YAP / FOS depletion in AKSP
  S4c  VAKSP DMSO vs FOLFIRI                     -> recorded for the FOLFIRI to-do
"""
import sys
import os
import csv
import openpyxl

SHEETS = ["Table S1c", "Table S1d", "Table S1f", "Table S1g",
          "Table S2c", "Table S2d", "Table S2e", "Table S3i", "Table S4c"]


def dump(ws, path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        for row in ws.iter_rows(values_only=True):
            w.writerow(["" if c is None else str(c).strip() for c in row])


def main():
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    wb = openpyxl.load_workbook(src, read_only=True)
    for name in SHEETS:
        if name not in wb.sheetnames:
            print(f"MISSING {name}")
            continue
        out = os.path.join(outdir, name.replace(" ", "_") + ".tsv")
        dump(wb[name], out)
        print(f"{os.path.getsize(out):>10}  {out}")
    wb.close()


if __name__ == "__main__":
    main()
