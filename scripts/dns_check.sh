#!/usr/bin/env bash
# Comprueba resolucion DNS de TARGET_HOST
set -euo pipefail

TARGET_HOST="${TARGET_HOST:-google.com}"
echo "Resolviendo: $TARGET_HOST"
getent hosts "$TARGET_HOST" || {
  echo "No se pudo resolver $TARGET_HOST"
  exit 1
}
