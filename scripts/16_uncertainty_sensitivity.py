"""Step 16: Uncertainty and sensitivity.
(a) Wilson 95% intervals for the university-sample shares.
(b) Sensitivity of the headline 'year the median community-college learner had access to a cybersecurity
    credential' to each judgment call: measure (annual vs cumulative), code definition, institution frame,
    and for-profit inclusion. Felt-need anchors change the latency, not the delivery year, so they are applied after.
Output: output/sensitivity.csv, output/intervals.csv
"""
import math, zipfile, pandas as pd
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return round(100*(c-h)), round(100*(c+h))
iv = []
for label, k, n in [("Universities with a credit-bearing cyber credential", 37, 50),
                    ("Of those, never under federal cyber codes through 2024", 7, 37),
                    ("Of those, hidden beyond normal lag or entirely (at least)", 15, 37),
                    ("Of independently dated & visible, lag > 3 years", 8, 18)]:
    lo, hi = wilson(k, n); iv.append(dict(measure=label, k=k, n=n, pct=round(100*k/n), ci95_low=lo, ci95_high=hi))
IV = pd.DataFrame(iv); IV.to_csv("output/intervals.csv", index=False); print(IV.to_string(index=False))

d = pd.read_csv("data/processed/completions_11_43.csv", dtype={"cipcode": str, "unitid": str})
iy = pd.read_csv("data/processed/inst_year.csv", dtype={"unitid": str, "sector": str})
z = zipfile.ZipFile("data/raw/HD2024.zip"); hd = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding="latin-1")
hd.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in hd.columns]
iy["instcat24"] = iy.unitid.map(hd.set_index("UNITID").INSTCAT); iy["control24"] = iy.unitid.map(hd.set_index("UNITID").CONTROL)
frames = {
  "Community colleges, incl. bachelor's-granting (headline)": ((iy.control24 == "1") & iy.instcat24.isin(["3", "4"])) | (iy.instcat24.isna() & (iy.sector == "4")),
  "Public 2-year sector only": iy.sector == "4",
  "All public + nonprofit institutions": iy.sector.isin(["1", "2", "4", "5", "7", "8"]),
  "All institutions incl. for-profit": iy.sector.notna(),
}
codes = {
  "Core: 11.1003, 43.0116/43.0403, 43.0404 (headline)": ["11.1003", "43.0116", "43.0403", "43.0404"],
  "Narrow: 11.1003 only": ["11.1003"],
  "Broad: core + 43.0303 critical infrastructure": ["11.1003", "43.0116", "43.0403", "43.0404", "43.0303"],
  "Very broad: core + networking codes": ["11.1003", "43.0116", "43.0403", "43.0404", "11.0901", "11.1001", "11.1002"],
}
f = d[(d.majornum == 1) & (d.awards > 0)]
def cross(frame_mask, codelist, measure):
    sub = iy[frame_mask].copy()
    off = f[f.cipcode.isin(codelist)][["year", "unitid"]].drop_duplicates()
    first = off.groupby("unitid").year.min()
    m = sub.merge(off.assign(a=1), on=["year", "unitid"], how="left").fillna({"a": 0})
    m["c"] = (m.unitid.map(first) <= m.year).astype(int)
    col = "a" if measure == "annual" else "c"
    g = m.assign(w=m[col] * m.total_awards_all_fields).groupby("year")[["w", "total_awards_all_fields"]].sum()
    s = g.w / g.total_awards_all_fields
    hit = s[s >= 0.5]
    return (int(hit.index.min()) if len(hit) else None), round(float(s.get(2024)), 2)
rows = []
H_FRAME = list(frames)[0]; H_CODES = list(codes)[0]
for measure in ["annual", "cumulative"]:
    yr, s24 = cross(frames[H_FRAME], codes[H_CODES], measure); rows.append(dict(varied="measure", setting=measure, median_year=yr, share_2024=s24))
for k, cl in codes.items():
    yr, s24 = cross(frames[H_FRAME], cl, "annual"); rows.append(dict(varied="code definition", setting=k, median_year=yr, share_2024=s24))
for k, fm in frames.items():
    yr, s24 = cross(fm, codes[H_CODES], "annual"); rows.append(dict(varied="institution frame", setting=k, median_year=yr, share_2024=s24))
S = pd.DataFrame(rows).drop_duplicates(["varied", "setting"]); S.to_csv("output/sensitivity.csv", index=False)
print(S.to_string(index=False))
