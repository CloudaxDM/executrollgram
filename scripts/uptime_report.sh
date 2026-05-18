#!/usr/bin/env bash
# Tiempo encendido y fecha de arranque
set -euo pipefail

echo "Fecha actual: $(date -Is)"
echo "Uptime: $(uptime -p 2>/dev/null || awk '{print $1 " segundos"}' /proc/uptime)"
echo "Desde: $(uptime -s 2>/dev/null || true)"
