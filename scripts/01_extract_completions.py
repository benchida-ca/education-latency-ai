"""Step 1: Extract IPEDS completions for computing-related programs (CIP 11.xx and 43.xx), 2003-2024.

What it does, in plain terms:
- Opens each year's IPEDS completions file (one row per institution x program x award level x major number).
- Uses the revised (_rv) file when NCES published one, since it corrects the original.
- Keeps only program codes starting with 11. (computer/IT) or 43. (security/protective services),
  so we can define 'networking' and 'cybersecurity' flexibly later.
- Finds the 'total awards' column, whose name changed over the years:
    2003-2007: CRACE24 (grand total); 2008 onward: CTOTALT, or men + women if CTOTALT is absent.
- Writes one combined table: data/processed/completions_11_43.csv
"""
import zipfile, io, sys
import pandas as pd

RAW = "data/raw"
rows = []
for y in range(2003, 2025):
    z = zipfile.ZipFile(f"{RAW}/C{y}_A.zip")
    names = z.namelist()
    rv = [n for n in names if "_rv" in n.lower()]
    name = rv[0] if rv else names[0]
    df = pd.read_csv(z.open(name), dtype=str, encoding="latin-1")
    df.columns = [c.strip().lstrip("﻿").lstrip("ï»¿").upper() for c in df.columns]
    df["CIPCODE"] = df["CIPCODE"].str.strip().str.strip('"')
    df = df[df["CIPCODE"].str.match(r"^(11|43)\.")].copy()
    if "CTOTALT" in df.columns:
        total = pd.to_numeric(df["CTOTALT"], errors="coerce")
        src = "CTOTALT"
    elif "CRACE24" in df.columns:
        total = pd.to_numeric(df["CRACE24"], errors="coerce")
        src = "CRACE24"
    else:
        total = pd.to_numeric(df["CTOTALM"], errors="coerce").fillna(0) + pd.to_numeric(df["CTOTALW"], errors="coerce").fillna(0)
        src = "CTOTALM+CTOTALW"
    out = pd.DataFrame({
        "year": y,
        "unitid": df["UNITID"].str.strip(),
        "cipcode": df["CIPCODE"],
        "majornum": pd.to_numeric(df["MAJORNUM"], errors="coerce"),
        "awlevel": pd.to_numeric(df["AWLEVEL"], errors="coerce"),
        "awards": total,
    })
    rows.append(out)
    print(y, name, src, len(out), "rows", int(out["awards"].sum()), "awards", flush=True)

pd.concat(rows).to_csv("data/processed/completions_11_43.csv", index=False)
print("written")
