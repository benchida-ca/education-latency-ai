#!/bin/bash
# Step 13: Wayback CDX harvest for one institution domain (gentle: one domain per call).
# Lists archived URLs (status 200, one row per unique URL = first capture) containing "cyber"
# or "information-security"/"infosec"/"information-assurance". Output: data/wayback/cdx/<domain>.txt
D="$1"
curl -sS -m 150 -G 'https://web.archive.org/cdx/search/cdx' --data-urlencode "url=$D" --data-urlencode 'matchType=domain' \
  --data-urlencode 'filter=original:.*([Cc]yber|[Ii]nformation-?[Ss]ecurity|[Ii]nfosec|[Ii]nformation-?[Aa]ssurance).*' \
  --data-urlencode 'filter=statuscode:200' --data-urlencode 'collapse=urlkey' --data-urlencode 'fl=timestamp,original' \
  --data-urlencode 'limit=3000' -o "data/wayback/cdx/$D.txt" -w "$D http=%{http_code} bytes=%{size_download} secs=%{time_total}\n"
