#!/usr/bin/env bash
# Crea un backup tar.gz de la carpeta de scripts
set -euo pipefail

SOURCE_DIR="${SOURCE_DIR:-/app/scripts}"
BACKUP_DIR="${BACKUP_DIR:-/tmp}"
OUTPUT="$BACKUP_DIR/scripts-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

tar -czf "$OUTPUT" -C "$SOURCE_DIR" .
echo "Backup creado: $OUTPUT"
ls -lh "$OUTPUT"
