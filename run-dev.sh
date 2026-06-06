#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

source venv/bin/activate

echo "Menjalankan ML Inference Service (Development Mode)..."
export ML_INFERENCE_DEBUG=true
exec python app.py
