#!/usr/bin/env bash
# Ficheros modificados recientemente en SCAN_PATH
set -euo pipefail

SCAN_PATH="${SCAN_PATH:-/app/scripts}"
MINUTES="${MINUTES:-1440}"

echo "Ruta: $SCAN_PATH"
echo "Ultimos minutos: $MINUTES"
find "$SCAN_PATH" -type f -mmin -"$MINUTES" -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort -r | head -50
