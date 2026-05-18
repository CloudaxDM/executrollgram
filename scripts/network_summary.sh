#!/usr/bin/env bash
# Resumen de red, DNS e interfaces
set -euo pipefail

echo "Host: $(hostname)"
echo
echo "DNS:"
cat /etc/resolv.conf 2>/dev/null || true
echo
echo "Interfaces:"
if command -v ip >/dev/null 2>&1; then
  ip -br addr
else
  cat /proc/net/dev
fi
