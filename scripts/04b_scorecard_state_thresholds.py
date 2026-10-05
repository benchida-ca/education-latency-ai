"""Step 4b: Scorecard value check with state-specific thresholds.
Thresholds: Financial Value Transparency / Gainful Employment earnings thresholds for calculation year 2024
(Federal Register 2024-31271, Dec 31 2024): median earnings of working adults aged 25-34 with only a high-school
diploma/GED, by state; national = $31,269. Program passes if graduates' median earnings exceed its state's threshold.
Applied to (a) earliest usable cohort file (1516_1617; 1-year earnings, EARN_MDN_HI_1YR) and
(b) Most-Recent cohorts (3-year earnings not enrolled, EARN_NE_MDN_3YR, closer to the rule's own timing).
Caveat: dollar years differ between earnings and thresholds; the rule itself uses program earnings 3 years out.
"""
import zipfile, pandas as pd
SC = "data/raw/College_Scorecard_Raw_Data_06032026/"
z = zipfile.ZipFile("data/raw/HD2024.zip"); hd = pd.read_csv(z.open(z.namelist()[0]), dtype=str, encoding="latin-1")
hd.columns = [c.strip().lstrip("﻿").replace("ï»¿", "").upper() for c in hd.columns]
abbr = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
th = pd.read_csv("data/processed/ge_state_thresholds_cy2024.csv").set_index("state").threshold
state_of = hd.set_index("UNITID").STABBR.map(abbr)
CTRL = {"Public": "Public", "Private, nonprofit": "Nonprofit", "Private, for-profit": "For-profit"}
LEV = {"1": "Certificate", "2": "Associate", "3": "Bachelor's"}
for f, col in [("FieldOfStudyData1516_1617_PP.csv", "EARN_MDN_HI_1YR"), ("Most-Recent-Cohorts-Field-of-Study.csv", "EARN_NE_MDN_3YR")]:
    df = pd.read_csv(SC + f, dtype=str, usecols=["UNITID", "CONTROL", "CIPCODE", "CREDLEV", col])
    df = df[df.CIPCODE.isin(["1109", "1110"]) & df.CREDLEV.isin(LEV)].copy()
    df["earn"] = pd.to_numeric(df[col], errors="coerce"); df = df[df.earn.notna()]
    df["thr"] = df.UNITID.map(state_of).map(th).fillna(th["United States"])
    df["pass"] = df.earn > df.thr
    g = df.groupby([df.CREDLEV.map(LEV), df.CONTROL.map(CTRL)]).agg(programs=("earn", "size"), median_earn=("earn", "median"), pass_rate=("pass", "mean"))
    g["pass_rate"] = (g.pass_rate * 100).round(0)
    print(f"\n=== {f} ({col}); state thresholds (national $31,269)"); print(g.to_string())
