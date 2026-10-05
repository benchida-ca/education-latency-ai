"""Step 5: Random sample of public 4-year universities for the catalog check.

Frame: IPEDS 2024 institutions in sector 1 (public, 4-year or above) that awarded at least
one bachelor's degree in any computing field (CIP 11.xx) in 2024 = 'computing-active'.
Sample: 50 institutions, fixed random seed (2026) so the draw is reproducible.
Also records each institution's web domain (HD2024 WEBADDR) and its first IPEDS award year
under the cyber codes (11.1003, 43.0116, 43.0403, 43.0404) at any level, and at bachelor's level.
Revision: frame restricted to INSTCAT 2 and own-domain campuses (see comments below).
"""
import zipfile, pandas as pd
d = pd.read_csv("data/processed/completions_11_43.csv", dtype={"cipcode": str, "unitid": str})
iy = pd.read_csv("data/processed/inst_year.csv", dtype={"unitid": str, "sector": str})
z = zipfile.ZipFile("data/raw/HD2024.zip"); hd = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding="latin-1")
hd.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in hd.columns]
f = d[(d.majornum == 1) & (d.awards > 0)]
active = set(f[(f.year == 2024) & (f.awlevel == 5) & f.cipcode.str.startswith("11.")].unitid)
frame = iy[(iy.year == 2024) & (iy.sector == "1") & iy.unitid.isin(active)].copy()
# Keep institutions that are primarily baccalaureate-or-above (INSTCAT 2). This drops community colleges
# that award a few bachelor's degrees (e.g., Lone Star, Austin CC), which IPEDS also files as 4-year.
cat = hd.set_index("UNITID")["INSTCAT"]
frame = frame[frame.unitid.map(cat) == "2"]
# Drop campuses whose web address is a sub-path of a parent site (their catalog is the parent's).
web = hd.set_index("UNITID")["WEBADDR"].fillna("")
frame = frame[~frame.unitid.map(web).str.replace("https://","").str.replace("http://","").str.rstrip("/").str.contains("/")]
print("frame size:", len(frame))
s = frame.sample(n=50, random_state=2026)
CY = ["11.1003", "43.0116", "43.0403", "43.0404"]
c = f[f.cipcode.isin(CY)]
s["ipeds_first_cyber_any"] = s.unitid.map(c.groupby("unitid").year.min())
s["ipeds_first_cyber_ba"] = s.unitid.map(c[c.awlevel == 5].groupby("unitid").year.min())
s["web"] = s.unitid.map(hd.set_index("UNITID")["WEBADDR"])
s[["unitid", "instnm", "stabbr", "total_awards_all_fields", "web", "ipeds_first_cyber_any", "ipeds_first_cyber_ba"]].to_csv("data/wayback/sample50.csv", index=False)
print(s[["instnm", "stabbr", "web", "ipeds_first_cyber_any", "ipeds_first_cyber_ba"]].to_string(index=False))
