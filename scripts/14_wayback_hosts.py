"""Step 14: Wayback CDX prefix scans by HOST (lighter than whole-domain scans) for the 50-university sample.
For each institution, scans www.<domain>/ and catalog.<domain>/ for archived URLs (status 200, first capture per URL)
whose address contains cyber / information-security / infosec / information-assurance.
Then flags 'program-like' URLs (contain program, degree, major, minor, concentration, catalog, curriculum, certificate,
track, option, academics, bachelor, master, b-s, bs-, ms-) and records the earliest one. Earliest capture is an UPPER bound
on when the institution publicly described something cyber; human/model review of the URL decides if it's a credential.
Resumable; stops after ~140s per run. Output: data/wayback/host_scans.csv (one row per host) and cdx/<host>.txt
"""
import csv, os, re, time, urllib.parse, urllib.request
import pandas as pd
s = pd.read_csv("data/wayback/sample50.csv", dtype=str)
def dom(w):
    w = re.sub(r"^https?://", "", str(w)).split("/")[0].lower()
    return re.sub(r"^www\.", "", w)
hosts = []
for _, r in s.iterrows():
    d = dom(r.web)
    base = d if d.count(".") >= 2 and not d.startswith("www.") and d.split(".")[0] not in ("www",) else d
    for h in sorted({f"www.{d}" if d.count(".") == 1 else d, f"catalog.{d}" if d.count(".") == 1 else f"catalog.{'.'.join(d.split('.')[-2:])}"}):
        hosts.append((r.unitid, r.instnm, h))
OUT = "data/wayback/host_scans.csv"; done = set()
if os.path.exists(OUT):
    prev = list(csv.DictReader(open(OUT)))
    done = {(x["unitid"], x["host"]) for x in prev if x["status"] == "ok"}
    from collections import Counter
    fails = Counter((x["unitid"], x["host"]) for x in prev if x["status"] != "ok" and "429" not in x["status"])
    done |= {k for k, v in fails.items() if v >= 2}  # give up on hosts too big for CDX (2+ timeouts)
PROG = re.compile(r"program|degree|major|minor|concentration|catalog|curricul|certificate|track|option|academics|bachelor|master|/b-?s|/m-?s|-bs|-ms|-ba|-mba|preview_program", re.I)
start = time.time(); new = not os.path.exists(OUT)
with open(OUT, "a", newline="") as fh:
    w = csv.writer(fh)
    if new: w.writerow(["unitid", "instnm", "host", "status", "n_urls", "earliest_any", "earliest_prog", "earliest_prog_url"])
    for uid, name, h in hosts:
        if (uid, h) in done: continue
        if time.time() - start > 140: break
        q = urllib.parse.urlencode([("url", h + "/"), ("matchType", "prefix"), ("filter", r"original:.*([Cc]yber|[Ii]nformation-?[Ss]ecurity|[Ii]nfosec|[Ii]nformation-?[Aa]ssurance).*"),
                                    ("filter", "statuscode:200"), ("collapse", "urlkey"), ("fl", "timestamp,original"), ("limit", "3000")])
        try:
            txt = urllib.request.urlopen("https://web.archive.org/cdx/search/cdx?" + q, timeout=110).read().decode("utf-8", "ignore")
            status = "ok"
        except Exception as e:
            txt, status = "", f"err:{str(e)[:40]}"
        rows = [l.split(" ", 1) for l in txt.splitlines() if " " in l]
        open(f"data/wayback/cdx/{h}.txt", "w").write(txt)
        rows.sort()
        prog = [r for r in rows if PROG.search(r[1])]
        w.writerow([uid, name, h, status, len(rows), rows[0][0][:8] if rows else "", prog[0][0][:8] if prog else "", prog[0][1] if prog else ""]); fh.flush()
        print(name, h, status, len(rows), prog[0][0][:4] if prog else "-", flush=True)
        if "429" in status: print("rate limited; stopping this run", flush=True); break
        time.sleep(10)
