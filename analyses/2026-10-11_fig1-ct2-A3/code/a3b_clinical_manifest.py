#!/usr/bin/env python3
"""A3b Stage C: per-patient clinical sample manifest for the pre/post-therapy cohorts (metadata only).

Sources (verified 2026-10-11; see docs/A3b_identity_clinical_contract_v0.2.md §3):
- Qin 2023 Cell Rep Med (PMC10591051): pre = colonoscopic biopsy <2 weeks before NAC (cryopreserved suspension);
  post = surgical resection, except two endoscopic post samples; response = TRG from Table S1 (hand-entered below).
- Chen 2024 Cancer Cell (GSE236581): GEO 'treatment stage' per sample (Pre/On/Post); the Roman suffix is a visit
  index, not a stage. Surgery / watch-and-wait from STAR Methods 'Human specimens'.
- Li 2023 Cancer Cell (GSE205506): suffix 3 = pre (-ICI), suffix 1/2 = post (+ICI, at curative resection);
  Atlas responder/non-responder = pCR/non-pCR (15/19 pCR, matching the paper).
Output: tables/metadata_gate/a3b_clinical_manifest.tsv (one row per patient x sample).
"""
import argparse
import re
from pathlib import Path

import pandas as pd

# Qin Table S1: TRG (0-3; None = not evaluable, endoscopic post sample).
QIN_TRG = {"XFZ02": 2, "XFZ03": 2, "XFZ05": 3, "XFZ07": 0, "XFZ08": 2, "XFZ09": 2, "XFZ17": 2, "XFZ18": 2,
           "XFZ19": 1, "XFZ21": None, "XFZ22": 0, "XFZ23": 3, "XFZ24": 1, "XFZ25": 2, "XFZ26": 2, "XFZ27": 2,
           "XFZ28": 1, "XFZ31": 2, "XFZ32": 2, "XFZ34": 3, "XFZ35": 2, "XFZ36": None, "XFZ38": 2, "XFZ39": 2,
           "XFZ41": 0, "XFZ44": 2, "XFZ46": 3, "XFZ48": 0, "XFZ49": 3}
QIN_ENDOSCOPIC_POST = {"XFZ21", "XFZ36"}

# Chen GEO treatment stage by patient and visit suffix (tumour samples; GSE236581 series matrix).
CHEN_STAGE = {
    "P01": {"I": "Pre", "II": "On", "III": "On", "IV": "Post"}, "P02": {"I": "Pre", "II": "Post"},
    "P03": {"I": "Pre", "II": "On", "III": "Post"}, "P04": {"I": "Pre", "II": "On", "III": "Post"},
    "P05": {"I": "Pre", "II": "Post"}, "P08": {"I": "Pre", "II": "On", "III": "On", "IV": "Post"},
    "P09": {"I": "Pre", "II": "Post"}, "P12": {"I": "Pre", "II": "Post"},
    "P14": {"I": "Pre", "II": "On", "III": "Post"}, "P15": {"I": "Pre", "II": "Post"},
    "P16": {"I": "Pre", "II": "Post"}, "P17": {"I": "Pre", "II": "Post"},
    "P18": {"I": "Pre", "II": "On", "III": "Post"}, "P19": {"I": "Pre", "II": "On", "III": "Post"},
    "P20": {"I": "Pre", "II": "On", "III": "Post"}, "P21": {"I": "Pre", "III": "Post"},
    "P22": {"I": "Pre", "II": "On", "III": "Post"}, "P23": {"I": "Pre", "II": "On", "III": "On", "IV": "Post"},
    "P25": {"I": "Pre", "II": "Post"}, "P26": {"I": "Pre", "II": "Post"}}
CHEN_NO_SURGERY = {"P08": "watch-and-wait (clinical CR)", "P09": "watch-and-wait (clinical CR)",
                   "P25": "refused surgery", "P02": "second-line, metastatic; died before surgery"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta", required=True, help="tables/metadata_gate/sample_metadata.tsv")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    s = pd.read_csv(a.meta, sep="\t")
    s = s[s.sample_type.isin(["primary tumor", "adjacent normal"])]
    rows = []
    for _, r in s[s.study_id == "Qin_2023_Cell_Rep_Med"].iterrows():
        pid = r.patient_id.split(".")[1]
        stage = "Pre" if r.treatment_status_before_resection == "naive" else "Post"
        trg = QIN_TRG.get(pid)
        rows.append(dict(
            stage=stage,
            specimen=("colonoscopic biopsy" if stage == "Pre" else
                      "endoscopic biopsy" if pid in QIN_ENDOSCOPIC_POST else "surgical resection"),
            response_system="TRG (pathological)", response=("NA" if trg is None else f"TRG{trg}"),
            residual_tumour=("unknown" if trg is None else "none" if trg == 0 else "yes"),
            source="Qin 2023 Methods + Table S1 (PMC10591051)", **_base(r)))
    for _, r in s[s.study_id == "Chen_2024_Cancer_Cell"].iterrows():
        pid = r.patient_id.split(".")[1]
        suf = re.search(r"_(I|II|III|IV)$", r.sample_id).group(1)
        stage = CHEN_STAGE[pid][suf]
        surg = CHEN_NO_SURGERY.get(pid)
        spec = ("colonoscopic biopsy" if stage != "Post" else
                f"biopsy ({surg})" if surg else "surgical specimen (inferred: final visit of a resected patient)")
        rows.append(dict(
            stage=stage, specimen=spec, response_system="composite iRECIST/pathology (CR includes cCR and MPR <10%)",
            response=r.RECIST, residual_tumour="unknown",
            source="GSE236581 stage; Chen 2024 STAR Methods", **_base(r)))
    for _, r in s[s.study_id == "Li_2023_Cancer_Cell"].iterrows():
        stage = "Pre" if r.treatment_status_before_resection == "naive" else "Post"
        pcr = r.treatment_response == "responder"
        rows.append(dict(
            stage=stage,
            specimen=("pre-treatment biopsy (inferred)" if stage == "Pre" else "curative surgical resection"),
            response_system="pathological (pCR)", response=("pCR" if pcr else "non-pCR"),
            residual_tumour=("none" if pcr else "yes"), source="Li 2023 Results/Methods; GSE205506", **_base(r)))
    m = pd.DataFrame(rows).sort_values(["study_id", "patient_id", "stage", "sample_id"])
    m.to_csv(a.out, sep="\t", index=False)
    print(m.groupby(["study_id", "sample_type", "stage"]).size().to_string())


def _base(r):
    return dict(study_id=r.study_id, patient_id=r.patient_id, sample_id=r.sample_id, sample_type=r.sample_type,
                atlas_status=r.treatment_status_before_resection, regimen=r.treatment_drug,
                msi=r.microsatellite_status, epi_total=r.epi_total, epi_median_umi=r.epi_median_umi)


if __name__ == "__main__":
    main()
