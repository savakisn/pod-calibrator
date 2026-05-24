#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Starting backend on :8000..."
cd "$ROOT/backend"
source venv/bin/activate
python -m src.main &
BACKEND_PID=$!

echo "Starting frontend on :3000..."
cd "$ROOT/frontend"
source /home/deck/miniconda3/etc/profile.d/conda.sh
conda activate frontend-env
npm run dev -- --hostname 0.0.0.0 --port 3000 &
FRONTEND_PID=$!

echo ""
echo "Running at http://10.0.0.121:3000"
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
