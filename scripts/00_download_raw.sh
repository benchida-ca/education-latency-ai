#!/bin/bash
# Step 0: Re-create data/raw from public sources (~4 GB). Run from the repo root.
# IPEDS completions (C) and institutional directory (HD) files, 2003-2024, from NCES:
mkdir -p data/raw && cd data/raw
for y in $(seq 2003 2024); do
  curl -sS -O "https://nces.ed.gov/ipeds/datacenter/data/C${y}_A.zip"
  curl -sS -O "https://nces.ed.gov/ipeds/datacenter/data/HD${y}.zip"
done
curl -sS -o CIPCode2020.csv https://nces.ed.gov/ipeds/cipcode/Files/CIPCode2020.csv
curl -sS -o Crosswalk2010to2020.csv https://nces.ed.gov/ipeds/cipcode/Files/Crosswalk2010to2020.csv
echo "College Scorecard: download the full raw data zip from https://collegescorecard.ed.gov/data/ (06/2026 release) and unzip here."
echo "NYT and GovInfo counts need free API keys saved as notes/nyt_key.txt and notes/govinfo_key.txt (never commit them)."
