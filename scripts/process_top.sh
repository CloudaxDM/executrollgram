#!/usr/bin/env bash
# Procesos que mas CPU o memoria consumen
set -euo pipefail

if command -v ps >/dev/null 2>&1; then
  echo "Top CPU:"
  ps -eo pid,ppid,pcpu,pmem,comm --sort=-pcpu | head -15
  echo
  echo "Top memoria:"
  ps -eo pid,ppid,pcpu,pmem,comm --sort=-pmem | head -15
else
  echo "ps no esta disponible en esta imagen"
fi
