#!/usr/bin/env bash
# Memoria disponible y limites del contenedor
set -euo pipefail

awk '
  /MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree/ { printf "%-16s %10.2f MiB\n", $1, $2 / 1024 }
' /proc/meminfo

echo
echo "Cgroup memory limit:"
if [[ -r /sys/fs/cgroup/memory.max ]]; then
  cat /sys/fs/cgroup/memory.max
elif [[ -r /sys/fs/cgroup/memory/memory.limit_in_bytes ]]; then
  cat /sys/fs/cgroup/memory/memory.limit_in_bytes
else
  echo "No detectado"
fi
