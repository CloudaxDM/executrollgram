#!/usr/bin/env bash
# Comprueba una URL con TARGET_URL
set -euo pipefail

TARGET_URL="${TARGET_URL:-https://example.com}"

python - <<PY
from urllib.request import Request, urlopen
url = "${TARGET_URL}"
req = Request(url, method="HEAD", headers={"User-Agent": "executrollgram"})
with urlopen(req, timeout=10) as response:
    print(f"{url} -> HTTP {response.status}")
PY
