# Walkthrough: understanding the pipeline (for Ben)

**Goal:** be able to say, truthfully, "I can explain every step and every judgment call." Plan for two sittings of about an hour each. Do Part A before submitting. Parts B-C are for interview prep.

---

## Part A: the core idea in code (before Monday, about 60 min)

### A1. Five pandas ideas (10 min)

Everything here is built from these five moves:

| Idea | What it does | Spreadsheet equivalent |
|---|---|---|
| `pd.read_csv(...)` | loads a table | open a file |
| `df[df.col == x]` | keeps rows matching a condition | filter |
| `df.groupby("year").awards.sum()` | totals by group | pivot table |
| `a.merge(b, on=["year","unitid"])` | joins two tables on shared keys | VLOOKUP |
| `(x * w).sum() / w.sum()` | weighted average | SUMPRODUCT / SUM |

### A2. Read the exercise script (15 min)

Open `scripts/exercise_my_definition.py`. It is the whole delivery measure in about 40 lines, numbered 1-5. In each step, find the pandas idea from A1.

### A3. Run it yourself (10 min)

From the Fellows Demo folder, run `python3 scripts/exercise_my_definition.py`. You should see 2023 as the first year at or above 50%. That is the headline number in Finding 1.

### A4. Change a judgment call (15 min)

Edit `MY_CODES` to add `"11.0901", "11.1001", "11.1002"` (networking). Rerun. The year jumps to 2009. Be able to explain why: some colleges file cybersecurity under networking codes (Las Positas), and networking programs were already widespread by 2003. That is exactly why the note reads the code-based date as an upper bound.

### A5. Say it out loud (10 min)

Explain the delivery measure in 3 sentences without notes. Something like: *"For each year, I take every community college, mark whether it awarded at least one credential under the cybersecurity codes, and weight it by how many credentials it awards overall. The weighted share is the fraction of learners attending a college that delivers the credential. The median learner has access when that share crosses 50%."*

---

## Part B: script by script (interview prep, about 60 min)

| Script | Plain-English job | The judgment call inside it | Likely question |
|---|---|---|---|
| 01 | Pulls 22 years of federal completion files and keeps computing/security programs | Use NCES's revised files; find the total column whose name changed in 2008 | "How did you know the totals were right?" Checked CS bachelor's against published totals (about 60K in 2004, 40K in 2010, 98K in 2020) and confirmed men + women = total in 100% of rows |
| 02 | Adds each college's state, sector, and total awards (the weight) | Total awards as a proxy for learners served | "Why not enrollment?" Awards are in the same files, are measured consistently, and track scale. Enrollment would be a robustness check |
| 11 | National and state clocks | Community-college definition (Trap 11); annual vs. ever-awarded | "Why include bachelor's-granting community colleges?" Florida and Washington would vanish otherwise |
| 04b | Earnings test vs. state thresholds | Use the federal gainful-employment thresholds rather than inventing one | "Isn't 1-year earnings too early?" Yes. The 3-year cohort points the same way, and the note flags the caveat |
| 05, 14 | Random university sample; Internet Archive evidence | Seed fixed for reproducibility; evidence dates are upper bounds | "How do you know the gaps aren't just graduation lag?" North Carolina shows normal lag of 1-4 years; I count only gaps beyond 3 |
| 06, 08 | NYT and Congressional Record counts | One source per layer; phrases preferred | "What went wrong?" Trap 8: two-word NYT searches fall back to one word |
| 16 | Intervals and sensitivity | Wilson intervals; vary every judgment call | "What would change your conclusion?" Only counting networking as cyber, which is itself evidence of hidden coding |

## Part C: questions to rehearse

1. Walk me through one data error you caught. (Pick Trap 1, 4, or 8.)
2. Why the median learner and not the first adopter?
3. What would you need to measure AI adoption properly? (Reading curricula at scale; the overlay problem.)
4. You don't write Python. How would you work as a fellow? (How you worked here: you set questions and definitions, the agent writes code, and you verify outputs against independent checks. Then show the exercise.)
5. What's the weakest part of this analysis? (Two cases from one era; codes undercount; web-evidence sample.)
