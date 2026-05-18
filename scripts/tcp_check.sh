#!/usr/bin/env bash
# Comprueba conexion TCP a TARGET_HOST y TARGET_PORT
set -euo pipefail

TARGET_HOST="${TARGET_HOST:-google.com}"
TARGET_PORT="${TARGET_PORT:-443}"

python - <<PY
import socket
host = "${TARGET_HOST}"
port = int("${TARGET_PORT}")
timeout = 5
with socket.create_connection((host, port), timeout=timeout):
    print(f"OK TCP {host}:{port}")
PY
