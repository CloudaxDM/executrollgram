#!/usr/bin/env bash
# Uso de disco de los puntos montados
set -euo pipefail

df -hT 2>/dev/null || df -h
