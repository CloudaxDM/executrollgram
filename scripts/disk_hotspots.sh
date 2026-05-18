#!/usr/bin/env bash
# Directorios que mas ocupan en SCAN_PATH
set -euo pipefail

SCAN_PATH="${SCAN_PATH:-/app}"
DEPTH="${DEPTH:-2}"

echo "Ruta: $SCAN_PATH"
echo "Profundidad: $DEPTH"
du -xh --max-depth="$DEPTH" "$SCAN_PATH" 2>/dev/null | sort -hr | head -30
