#!/usr/bin/env bash
# Resumen rapido de salud del contenedor
set -euo pipefail

echo "Host: $(hostname)"
echo "Fecha: $(date -Is)"
echo "Uptime: $(uptime 2>/dev/null || cat /proc/uptime)"
echo
echo "Disco:"
df -h / /app 2>/dev/null || df -h
echo
echo "Carga:"
cat /proc/loadavg
