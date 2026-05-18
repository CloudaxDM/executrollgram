#!/usr/bin/env bash
# Montajes visibles dentro del contenedor
set -euo pipefail

if command -v findmnt >/dev/null 2>&1; then
  findmnt
else
  mount
fi
