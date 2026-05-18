#!/usr/bin/env bash
# Carga CPU y numero de cores visibles
set -euo pipefail

echo "Load average: $(cat /proc/loadavg)"
echo "CPU cores visibles: $(getconf _NPROCESSORS_ONLN 2>/dev/null || grep -c '^processor' /proc/cpuinfo)"
echo
grep -m1 'model name' /proc/cpuinfo 2>/dev/null || true
