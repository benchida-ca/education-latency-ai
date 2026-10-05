# Latency: How Long American Education Takes to Respond to New Jobs

**Author:** Ben Chida · **Status:** research note and replication materials, October 2026 · **Read the note:** [`Latency_Research_Note.pdf`](Latency_Research_Note.pdf)

When a new kind of job emerges, how long does it take for a credential with labor-market value to reach the median learner? This repository measures that latency for two cases, networking (late 1990s) and cybersecurity (late 2000s), using public federal data. It asks what the answer implies for AI.

**Headline findings:**

1. **Felt need reached insiders first and the workforce system last.** For networking, Congress, the press, and federal agencies moved within about two years. For cybersecurity, Congress turned to the issue about seven years before the press and agencies, and the Labor Department's workforce agency about 18 years after Congress.
2. **Enactment came fast, but early policy aimed elsewhere.** Political latency was a year or two. Early federal programs targeted research universities and federal service rather than the median learner.
3. **Implementation took roughly 9 to 14 years.** The median community-college learner reached a networking credential around 2009 and a cybersecurity credential in 2023.
4. **For-profits filled the gap, with weak value below the bachelor's.** For-profit colleges produced 78% of cybersecurity credentials in 2005. Below the bachelor's level, their programs cleared a state earnings bar far less often than public ones.
5. **Federal data misses much of the adaptation.** In a random sample of 50 public universities, at least 41% of those with cybersecurity credentials (95% interval 26–57%) were invisible to federal cybersecurity codes for years beyond normal lag, or entirely.
6. **State latencies differ by more than a decade,** from 2011 (Georgia) to after 2024 (four states).

## How this was built

I designed the questions, definitions, and judgment calls. An AI coding agent (Claude) wrote and ran the code under my direction. Every step is logged:

- `DECISIONS.md` lists the judgment calls I made and why.
- `notes/lab-notebook.md` is the running log: what was tried, what broke, and the 12 data traps found and fixed.
- `WALKTHROUGH.md` is a plain-English guide to every script.
- `HAND_VALIDATION.md` records the hand check of 8 universities behind Finding 5.
- Each script opens with a plain-English description of what it does.

## Repository map

| Path | What it holds |
|---|---|
| `scripts/00_download_raw.sh` | Re-downloads the raw public data (~4 GB, not stored here) |
| `scripts/01`–`02` | Build the IPEDS completions and institution tables |
| `scripts/03`, `11`, `12`, `17` | Implementation latency, nationally and by state |
| `scripts/04`, `04b` | Labor-market value check (College Scorecard, state earnings thresholds) |
| `scripts/05`, `13`–`15` | Random sample of 50 universities; Internet Archive evidence; gap chart |
| `scripts/06`, `08` | Felt need: NYT and Congressional Record counts |
| `scripts/07`, `09`, `10` | Felt-need and enactment-timeline charts |
| `scripts/16` | Confidence intervals and sensitivity table |
| `data/processed/` | Every derived table the note cites |
| `data/wayback/` | University-sample coding and Internet Archive evidence |
| `output/` | Charts, intervals, sensitivity. Charts marked "prototype" or "preliminary" are early working versions; the note's figures are final. |

## Sources

- IPEDS completions and directory, 2003–2024 (NCES)
- College Scorecard field-of-study data, 06/2026 release
- FVT/GE earnings thresholds, 2024 (Federal Register 2024-31271)
- NYT Article Search API
- GovInfo Congressional Record and hearings
- Federal Register API
- North Carolina Community College System approval reports, 2007–2013
- Internet Archive Wayback Machine

## Replicating

1. Run `scripts/00_download_raw.sh`.
2. Download the Scorecard zip.
3. Save the API keys as described in that script.
4. Run the numbered scripts in order with Python 3 and pandas.

Steps 06, 08, and 14 call rate-limited APIs. They are resumable and may take several runs.
