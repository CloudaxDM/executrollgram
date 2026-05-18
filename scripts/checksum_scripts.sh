#!/usr/bin/env bash
# Calcula checksums SHA256 de los scripts
set -euo pipefail

SOURCE_DIR="${SOURCE_DIR:-/app/scripts}"
find "$SOURCE_DIR" -maxdepth 1 -type f -print0 2>/dev/null | sort -z | xargs -0 sha256sum
