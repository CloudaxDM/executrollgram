#!/usr/bin/env bash
# Variables de entorno ocultando secretos comunes
set -euo pipefail

env | sort | grep -Evi '(TOKEN|SECRET|PASSWORD|PASS|KEY|AUTH|COOKIE|CREDENTIAL)'
