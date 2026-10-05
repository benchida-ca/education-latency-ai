"""Step 8: Political-layer sensor - Congressional Record (CREC) and committee hearings (CHRG) via GovInfo search API.

Counts are 'granules' (CREC: individual speeches/items; CHRG: hearing documents) whose text matches the query,
per calendar year by publish date. CREC total per year is also pulled, so CREC can be normalized (share of items).
Caveat: CHRG publish dates often lag the hearing itself by months to a couple of years.
Resumable: skips (series, year) already saved; stops after ~150 seconds.
Output: data/processed/congress_counts.csv
"""
import json, os, csv, time, urllib.request
K = open("notes/govinfo_key.txt").read().strip()
OUT = "data/processed/congress_counts.csv"
CY = '("cybersecurity" OR "cyber security")'
SERIES = {
    "crec_total": "collection:CREC",
    "crec_cyber": f"collection:CREC AND {CY}",
    "crec_computer_security": 'collection:CREC AND "computer security"',
    "crec_cyber_workforce": f'collection:CREC AND {CY} AND (workforce OR "workforce development" OR "skilled workers")',
    "crec_it_workers": 'collection:CREC AND ("information technology workers" OR "IT workers" OR "high-tech workers" OR "information technology workforce")',
    "crec_network_admin": 'collection:CREC AND ("network administrators" OR "computer networking")',
    "chrg_cyber": f"collection:CHRG AND {CY}",
    "chrg_cyber_workforce": f'collection:CHRG AND {CY} AND (workforce OR "workforce development")',
    "chrg_it_workers": 'collection:CHRG AND ("information technology workers" OR "IT workers" OR "high-tech workers" OR "information technology workforce")',
}
done = set()
if os.path.exists(OUT):
    for r in csv.DictReader(open(OUT)): done.add((r["series"], r["year"]))
todo = [(s, y) for s in SERIES for y in range(1994, 2025) if (s, str(y)) not in done]
print(len(todo), "remaining", flush=True)
start = time.time(); new = not os.path.exists(OUT)
with open(OUT, "a", newline="") as fh:
    w = csv.writer(fh)
    if new: w.writerow(["series", "year", "count"])
    for s, y in todo:
        if time.time() - start > 150: break
        q = f"{SERIES[s]} AND publishdate:range({y}-01-01,{y}-12-31)"
        req = urllib.request.Request("https://api.govinfo.gov/search?api_key=" + K,
              data=json.dumps({"query": q, "pageSize": 1, "offsetMark": "*"}).encode(), headers={"Content-Type": "application/json"})
        try:
            c = json.load(urllib.request.urlopen(req, timeout=40)).get("count")
        except Exception as e:
            print("error", s, y, e, flush=True); time.sleep(5); continue
        w.writerow([s, y, c]); fh.flush()
        time.sleep(0.6)
print("done this run", flush=True)
