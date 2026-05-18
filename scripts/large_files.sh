#!/usr/bin/env bash
# Ficheros mas grandes en SCAN_PATH
set -euo pipefail

SCAN_PATH="${SCAN_PATH:-/app/scripts}"
echo "Ruta: $SCAN_PATH"
find "$SCAN_PATH" -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -30 | awk '{ printf "%.2f MiB  ", $1 / 1024 / 1024; $1=""; print substr($0,2) }'
