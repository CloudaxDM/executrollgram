#!/usr/bin/env bash
# Limites cgroup de CPU, memoria y procesos
set -euo pipefail

echo "CPU max:"
cat /sys/fs/cgroup/cpu.max 2>/dev/null || echo "No detectado"
echo
echo "Memory max:"
cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null || echo "No detectado"
echo
echo "PIDs max:"
cat /sys/fs/cgroup/pids.max 2>/dev/null || echo "No detectado"
