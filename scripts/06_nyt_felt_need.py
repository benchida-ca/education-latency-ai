"""Step 6: Felt-need discourse in the New York Times, 1990-2024 (Article Search API, hit counts only).

Each query counts NYT articles per year that match the terms. Notes on the API (learned by testing):
- q with several words behaves like AND ("cybersecurity workers" = both words), quoted phrases work,
  and OR / body: filters are NOT supported, so each term is its own series.
- Rate limit is ~5 requests/minute, so the script sleeps 12.5s between calls and is resumable:
  it skips (series, year) pairs already saved and stops after ~13 calls per run (fits one 3-minute window).
- No usable yearly total: q=* returns 0, an empty q is capped at 10,000 hits, and 'the' is treated as a stopword.
  So counts are raw. We read timing (onset and inflection), not levels.
Output: data/processed/nyt_counts.csv
"""
import json, os, time, urllib.parse, urllib.request, csv, sys
KEY = open("notes/nyt_key.txt").read().strip()
OUT = "data/processed/nyt_counts.csv"
SERIES = {
    "cybersecurity": "cybersecurity",
    "cyber_security_phrase": '"cyber security"',
    "computer_security_phrase": '"computer security"',
    "cyber_workers": "cybersecurity workers",
    "it_workers_phrase": '"information technology workers"',
    "network_admin": '"network administrators"',
}
done = set()
if os.path.exists(OUT):
    for r in csv.DictReader(open(OUT)): done.add((r["series"], r["year"]))
todo = [(s, y) for s in SERIES for y in range(1990, 2025) if (s, str(y)) not in done]
print(len(todo), "remaining")
budget = int(sys.argv[1]) if len(sys.argv) > 1 else 13
new = not os.path.exists(OUT)
with open(OUT, "a", newline="") as fh:
    w = csv.writer(fh)
    if new: w.writerow(["series", "query", "year", "hits"])
    for s, y in todo[:budget]:
        params = urllib.parse.urlencode({"q": SERIES[s], "begin_date": f"{y}0101", "end_date": f"{y}1231", "api-key": KEY})
        try:
            d = json.load(urllib.request.urlopen("https://api.nytimes.com/svc/search/v2/articlesearch.json?" + params, timeout=30))
            hits = (d.get("response", {}).get("metadata") or d.get("response", {}).get("meta", {})).get("hits")
            w.writerow([s, SERIES[s], y, hits]); fh.flush(); print(s, y, hits, flush=True)
        except Exception as e:
            print("error", s, y, e, flush=True); break
        time.sleep(12.5)
