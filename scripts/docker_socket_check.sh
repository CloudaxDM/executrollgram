#!/usr/bin/env bash
# Comprueba si el socket Docker esta montado
set -euo pipefail

SOCKET="/var/run/docker.sock"
if [[ -S "$SOCKET" ]]; then
  echo "ATENCION: $SOCKET esta montado. Los scripts podrian controlar Docker del host."
  ls -l "$SOCKET"
  exit 2
fi

echo "OK: no se detecta $SOCKET"
