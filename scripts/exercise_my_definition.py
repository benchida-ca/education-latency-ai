"""EXERCISE (for Ben): change a judgment call yourself and see what moves.

Edit the two settings below, save, and run:   python3 scripts/exercise_my_definition.py
It prints, for each year, the share of community-college learners at a college that awarded a credential
under YOUR code list, and the first year that share reached 50%.

Ideas to try:
  1. Add networking codes to the cybersecurity list (what happens to the year? why?)
  2. Use only '11.1003' (narrowest definition)
  3. Set MEASURE = 'cumulative' (has ever awarded vs. awarded this year)
"""
import zipfile
import pandas as pd

# ---- YOUR SETTINGS -------------------------------------------------------
MY_CODES = ["11.1003", "43.0116", "43.0403", "43.0404"]   # program codes that count as "cybersecurity"
MEASURE = "annual"                                          # "annual" or "cumulative"
# --------------------------------------------------------------------------

# 1. Load the two tables the pipeline built (one row per institution x program x year; one row per institution x year)
completions = pd.read_csv("data/processed/completions_11_43.csv", dtype={"cipcode": str, "unitid": str})
institutions = pd.read_csv("data/processed/inst_year.csv", dtype={"unitid": str, "sector": str})

# 2. Decide which institutions are community colleges (public, not primarily bachelor's-granting, per the 2024 directory)
z = zipfile.ZipFile("data/raw/HD2024.zip")
hd = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding="latin-1")
hd.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in hd.columns]
category = hd.set_index("UNITID")["INSTCAT"]
control = hd.set_index("UNITID")["CONTROL"]
institutions["is_cc"] = ((institutions.unitid.map(control) == "1") & institutions.unitid.map(category).isin(["3", "4"])) \
    | (institutions.unitid.map(category).isna() & (institutions.sector == "4"))
cc = institutions[institutions.is_cc]

# 3. Which colleges awarded at least one credential under MY_CODES in each year? (first majors only)
awarded = completions[(completions.majornum == 1) & (completions.awards > 0) & completions.cipcode.isin(MY_CODES)]
offers = awarded[["year", "unitid"]].drop_duplicates().assign(offers=1)
first_year = offers.groupby("unitid").year.min()

# 4. Attach that to every community college-year; colleges with no awards get 0
table = cc.merge(offers, on=["year", "unitid"], how="left").fillna({"offers": 0})
if MEASURE == "cumulative":
    table["offers"] = (table.unitid.map(first_year) <= table.year).astype(int)

# 5. Weighted share: each college counts by its total awards in all fields (a proxy for how many learners it serves)
table["weighted"] = table.offers * table.total_awards_all_fields
by_year = table.groupby("year")[["weighted", "total_awards_all_fields"]].sum()
share = by_year.weighted / by_year.total_awards_all_fields

print((share * 100).round(1).to_string())
crossed = share[share >= 0.5]
print("\nFirst year at or above 50%:", int(crossed.index.min()) if len(crossed) else "not reached")
