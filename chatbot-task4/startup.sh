#!/usr/bin/env bash
set -euo pipefail

# Azure App Service provides PORT; default to 8000 for local/prod parity.
PORT="${PORT:-8000}"

exec gunicorn --workers 2 --threads 4 --bind "0.0.0.0:${PORT}" "app:app"

