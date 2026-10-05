# Walkthrough: how the pipeline works

A plain-English guide to the code, for readers who want to check the measure or change a judgment call themselves.

## Part A: the core measure in about 40 lines

### A1. Five pandas ideas

Everything here is built from these five moves:

| Idea | What it does | Spreadsheet equivalent |
|---|---|---|
| `pd.read_csv(...)` | loads a table | open a file |
| `df[df.col == x]` | keeps rows matching a condition | filter |
| `df.groupby("year").awards.sum()` | totals by group | pivot table |
| `a.merge(b, on=["year","unitid"])` | joins two tables on shared keys | VLOOKUP |
| `(x * w).sum() / w.sum()` | weighted average | SUMPRODUCT / SUM |

### A2. Read the exercise script

`scripts/exercise_my_definition.py` is the whole implementation measure, in five numbered steps. Each step uses one or two of the ideas above.

### A3. Run it

From the repository root, after running `scripts/00_download_raw.sh` and scripts 01–02, run `python3 scripts/exercise_my_definition.py`. It prints the access-weighted share for each year; 2023 is the first year at or above 50%, the cybersecurity date in Finding 3.

### A4. Change a judgment call

Edit `MY_CODES` to add `"11.0901", "11.1001", "11.1002"` (networking) and rerun. The year jumps to 2009. Some colleges file cybersecurity under networking codes (Las Positas, for example), and networking programs were already widespread by 2003. That is why the note reads the code-based date as an upper bound.

### A5. The measure in three sentences

For each year, take every community college, mark whether it awarded at least one credential under the cybersecurity codes, and weight it by how many credentials it awards overall. The weighted share is the fraction of learners attending a college that delivers the credential. The median learner has access when that share crosses 50%.

## Part B: script by script

| Script | What it does | The judgment call inside it | A question a reader might ask |
|---|---|---|---|
| 01 | Pulls 22 years of federal completion files and keeps computing and security programs | Use NCES's revised files; find the total column whose name changed in 2008 | *How do you know the totals are right?* Computer-science bachelor's totals match published figures (about 60K in 2004, 40K in 2010, 98K in 2020), and men + women = total in 100% of rows. |
| 02 | Adds each college's state, sector, and total awards (the weight) | Total awards as a proxy for learners served | *Why not enrollment?* Awards are in the same files, are measured consistently, and track scale. Enrollment would be a robustness check. |
| 11 | National and state latencies | Community-college definition (Trap 11); annual vs. ever-awarded measure | *Why include bachelor's-granting community colleges?* Florida's and much of Washington's systems would otherwise vanish. |
| 04b | Earnings test against state thresholds | Use the federal gainful-employment thresholds rather than inventing one | *Isn't one-year earnings too early?* Yes. The three-year cohorts point the same way, and the note flags the caveat. |
| 05, 14 | Random university sample; Internet Archive evidence | Fixed seed for reproducibility; evidence dates are upper bounds | *Couldn't the gaps just be graduation lag?* North Carolina records show a normal lag of 1–4 years; only gaps beyond 3 years are counted. |
| 06, 08 | New York Times and Congressional Record counts | One source per layer; exact phrases preferred | *What went wrong along the way?* Trap 8: two-word NYT searches silently fall back to one word. |
| 16 | Intervals and sensitivity | Wilson intervals; vary every judgment call | *What would change the conclusion?* Only counting networking programs as cybersecurity, which is itself evidence of hidden coding. |
| 17 | Finding 3 chart | Felt-need bands from Finding 1 | — |
