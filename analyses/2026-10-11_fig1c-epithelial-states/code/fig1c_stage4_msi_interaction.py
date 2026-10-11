import sys, glob, numpy as np, pandas as pd
R="/home/zz950/DATA/HotData/TWEAKR-oncoFetal/analysis/fig1c_epi_states_20261011"
sys.path.insert(0, R+"/code")
from fig1c_stage3 import reml_hk, patient_median
s3 = pd.concat([pd.read_csv(f, sep="\t") for f in sorted(glob.glob(R+"/stage3/sample/*.s3_contrasts.private.tsv.gz"))])
meta = pd.read_csv("/home/zz950/DATA/scRNAseq/meta_study/CRC_metadata_extraction/patient_characteristics/crc_patient_metadata.tsv", sep="\t", usecols=["patient_id","msi_status"])
e = s3[(s3.contrast=="pro_vs_rev") & s3.eligible]
pv = patient_median(e, "final").merge(meta, on="patient_id", how="left")
rows=[]
for s, x in pv.groupby("study_id"):
    h, m = x[x.msi_status=="MSI-H"].v, x[x.msi_status=="MSS"].v
    if len(h)>=5 and len(m)>=5:
        rows.append({"study_id":s,"n_msih":len(h),"n_mss":len(m),"diff":h.mean()-m.mean(),
                     "se":np.sqrt(h.var(ddof=1)/len(h)+m.var(ddof=1)/len(m))})
st=pd.DataFrame(rows); r=reml_hk(st["diff"], st.se)
out=st.assign(contrast="pro_vs_rev")
out.loc[len(out)]={"study_id":"POOLED","n_msih":int(st.n_msih.sum()),"n_mss":int(st.n_mss.sum()),"diff":r["estimate"],"se":r["se_hk"],"contrast":"pro_vs_rev"}
out["ci_low"]=np.nan; out["ci_high"]=np.nan; out["p"]=np.nan; out["I2"]=np.nan
out.loc[out.study_id=="POOLED",["ci_low","ci_high","p","I2"]]=[r["ci_low"],r["ci_high"],r["p"],r["I2"]]
out.to_csv(R+"/stage4/public/S4_msi_interaction.tsv", sep="\t", index=False)
print(out.round(4).to_string())
