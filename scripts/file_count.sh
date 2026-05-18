#!/usr/bin/env bash
# Cuenta ficheros por extension en SCAN_PATH
set -euo pipefail

SCAN_PATH="${SCAN_PATH:-/app/scripts}"
echo "Ruta: $SCAN_PATH"
find "$SCAN_PATH" -type f 2>/dev/null \
  | awk '
      { n=$0; sub(/^.*\//, "", n); if (n ~ /\./) { sub(/^.*\./, ".", n) } else { n="[sin_extension]" } count[n]++ }
      END { for (ext in count) print count[ext], ext }
    ' \
  | sort -nr
