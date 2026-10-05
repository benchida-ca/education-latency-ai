"""Step 2: Institution-level context for each year, 2003-2024.

- Total awards across ALL fields at each institution (IPEDS reports this under program code '99').
  We use it as the 'access weight': a college that graduates 5,000 people a year counts for more
  learners than one that graduates 50.
- Institution directory (HD files): name, state, sector (public/private, 2-year/4-year), level.
Output: data/processed/inst_year.csv
"""
import zipfile
import pandas as pd

RAW = "data/raw"
def read(zpath):
    z = zipfile.ZipFile(zpath); ns = z.namelist()
    n = ([x for x in ns if "_rv" in x.lower()] or ns)[0]
    df = pd.read_csv(z.open(n), dtype=str, encoding="latin-1")
    df.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in df.columns]
    return df

out = []
for y in range(2003, 2025):
    c = read(f"{RAW}/C{y}_A.zip")
    c["CIPCODE"] = c["CIPCODE"].str.strip().str.strip('"')
    tcol = "CTOTALT" if "CTOTALT" in c.columns else "CRACE24"
    t = c[(c["CIPCODE"].isin(["99", "99.0000"])) & (pd.to_numeric(c["MAJORNUM"]) == 1)].copy()
    t["tot"] = pd.to_numeric(t[tcol], errors="coerce")
    tot = t.groupby("UNITID")["tot"].sum().rename("total_awards_all_fields")
    hd = read(f"{RAW}/HD{y}.zip")
    keep = [k for k in ["UNITID", "INSTNM", "STABBR", "SECTOR", "ICLEVEL", "CONTROL"] if k in hd.columns]
    hd = hd[keep].set_index("UNITID")
    m = hd.join(tot, how="inner").reset_index()
    m["year"] = y
    out.append(m)
    print(y, len(m), "institutions with completions;", int(m.total_awards_all_fields.sum()), "total awards", flush=True)
pd.concat(out).rename(columns=str.lower).to_csv("data/processed/inst_year.csv", index=False)
print("written")
