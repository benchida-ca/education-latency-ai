"""Step 4: Does 'public/nonprofit' work as a proxy for labor-market value?

Source: College Scorecard field-of-study files (program = institution x 4-digit CIP x credential level).
Measure: EARN_NE_MDN_3YR = median earnings of graduates who are working and not enrolled, 3 years after completing.
Test (adapted from the 2023 financial value / gainful-employment 'earnings premium' idea):
  does the program's median beat a typical high-school graduate's earnings?
  v1 uses a single national threshold of $28,000 (Scorecard's own 'threshold earnings' figure).
  The actual rule uses state-specific thresholds for HS graduates aged 25-34; refine later.
Caveat: at the 4-digit level, cybersecurity (11.1003) is grouped with networking management, sysadmin,
web management, and support (all 11.10). So this checks the IT/security family as a whole.
"""
import pandas as pd
SC = "data/raw/College_Scorecard_Raw_Data_06032026/"
FAM = {"1109": "Networking (11.09)", "1110": "IT admin/security (11.10)", "4304": "Security sci/tech (43.04)", "4301": "Criminal justice (43.01, comparison)"}
CTRL = {"Public": "Public", "Private, nonprofit": "Nonprofit", "Private, for-profit": "For-profit", "1": "Public", "2": "Nonprofit", "3": "For-profit"}
LEV = {"1": "Undergrad certificate", "2": "Associate", "3": "Bachelor's"}
THRESH = 28000
for f in ["FieldOfStudyData1415_1516_PP.csv", "Most-Recent-Cohorts-Field-of-Study.csv"]:
    df = pd.read_csv(SC + f, dtype=str, usecols=["UNITID", "INSTNM", "CONTROL", "CIPCODE", "CREDLEV", "EARN_NE_MDN_3YR"])
    df = df[df.CIPCODE.isin(FAM) & df.CREDLEV.isin(LEV)].copy()
    df["earn"] = pd.to_numeric(df.EARN_NE_MDN_3YR, errors="coerce")
    df["has"] = df.earn.notna()
    df["pass"] = df.earn > THRESH
    g = df.groupby([df.CIPCODE.map(FAM), df.CONTROL.map(CTRL)]).agg(
        programs=("UNITID", "size"), with_earnings=("has", "sum"),
        median_earn=("earn", "median"), pass_n=("pass", "sum"))
    g["pass_rate_%"] = (g.pass_n / g.with_earnings * 100).round(0)
    print(f"\n=== {f}  (threshold ${THRESH:,})")
    print(g.drop(columns="pass_n").to_string())
    if "Most-Recent" in f:
        lv = df[df.CIPCODE.isin(["1110", "1109"])].groupby([df.CREDLEV.map(LEV), df.CONTROL.map(CTRL)]).agg(
            programs=("UNITID", "size"), with_earnings=("has", "sum"), median_earn=("earn", "median"), pass_n=("pass", "sum"))
        lv["pass_rate_%"] = (lv.pass_n / lv.with_earnings * 100).round(0)
        print("\nNetworking + IT admin/security, by credential level:"); print(lv.drop(columns="pass_n").to_string())
        ful = df[df.INSTNM.str.contains("Fullerton", na=False) & df.CIPCODE.isin(FAM)]
        print("\nCSU Fullerton check:"); print(ful[["INSTNM", "CIPCODE", "CREDLEV", "earn"]].to_string(index=False))
