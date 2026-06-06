#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

source venv/bin/activate

echo "Menjalankan ML Inference Service dengan Gunicorn..."
exec gunicorn -w 4 -b 0.0.0.0:5001 app:app --access-logfile -
