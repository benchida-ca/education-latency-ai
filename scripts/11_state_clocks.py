"""Step 11: State-by-state delivery clocks for cybersecurity and networking (community colleges).

Community college definition (revised, Trap 11): public institutions whose 2024 IPEDS INSTCAT is 3 or 4
("not primarily baccalaureate" or "associate's and certificates"). This adds ~230 bachelor's-granting
community colleges (e.g., Florida College System, many in WA) that IPEDS files as 4-year (sector 1).
Institutions that closed before 2024 fall back to sector 4 (public 2-year).

Two delivery measures, both access-weighted by each college's total awards (all fields) that year:
  annual   = college awarded >=1 credential in the case's codes THAT year (noisy)
  cumulative = college has awarded one at least once by that year (diffusion timing; ignores closures)
Outputs: data/processed/state_clocks.csv (crossing years) and state_curves.csv (yearly shares)
"""
import zipfile, pandas as pd
d = pd.read_csv("data/processed/completions_11_43.csv", dtype={"cipcode": str, "unitid": str})
iy = pd.read_csv("data/processed/inst_year.csv", dtype={"unitid": str, "sector": str})
z = zipfile.ZipFile("data/raw/HD2024.zip"); hd = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding="latin-1")
hd.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in hd.columns]
cat24 = hd.set_index("UNITID")["INSTCAT"]; ctl24 = hd.set_index("UNITID")["CONTROL"]
iy["instcat24"] = iy.unitid.map(cat24); iy["control24"] = iy.unitid.map(ctl24)
iy["cc"] = ((iy.control24 == "1") & iy.instcat24.isin(["3", "4"])) | (iy.instcat24.isna() & (iy.sector == "4"))
cc = iy[iy.cc].copy()
DEFS = {"cyber": ["11.1003", "43.0116", "43.0403", "43.0404"], "net": ["11.0901", "11.1001", "11.1002"]}
f = d[(d.majornum == 1) & (d.awards > 0)]
curves = []
for case, codes in DEFS.items():
    off = f[f.cipcode.isin(codes)][["year", "unitid"]].drop_duplicates()
    first = off.groupby("unitid").year.min()
    m = cc.merge(off.assign(annual=1), on=["year", "unitid"], how="left").fillna({"annual": 0})
    m["cumulative"] = (m.unitid.map(first) <= m.year).astype(int)
    for geo, sub in [("US", m)] + list(m.groupby("stabbr")):
        w = sub.total_awards_all_fields
        g = sub.assign(wa=sub.annual * w, wc=sub.cumulative * w).groupby("year")[["wa", "wc", "total_awards_all_fields"]].sum()
        g["annual"] = g.wa / g.total_awards_all_fields; g["cumulative"] = g.wc / g.total_awards_all_fields
        g["n_colleges"] = sub.groupby("year").unitid.nunique()
        curves.append(g[["annual", "cumulative", "n_colleges"]].assign(case=case, geo=geo).reset_index())
C = pd.concat(curves); C.to_csv("data/processed/state_curves.csv", index=False)
def cross(s, t):
    hit = s[s >= t]; return int(hit.index.min()) if len(hit) else None
rows = []
for (case, geo), g in C.groupby(["case", "geo"]):
    g = g.set_index("year")
    rows.append(dict(case=case, geo=geo, colleges_2024=int(g.n_colleges.get(2024, 0)),
        cum_2010=round(g.cumulative.get(2010, float("nan")), 2), cum_2024=round(g.cumulative.get(2024, float("nan")), 2),
        cum_year_25=cross(g.cumulative, .25), cum_year_50=cross(g.cumulative, .5),
        ann_year_50=cross(g.annual, .5), ann_2024=round(g.annual.get(2024, float("nan")), 2)))
R = pd.DataFrame(rows); R.to_csv("data/processed/state_clocks.csv", index=False)
print("community colleges in frame (2024):", cc[cc.year == 2024].unitid.nunique())
print(R[R.geo == "US"].to_string(index=False))
