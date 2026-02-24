#!/bin/bash
set -e

MODE=${1:-dev}

if [[ "$MODE" != "dev" && "$MODE" != "production" ]]; then
  echo "Usage: ./scripts/run.sh [dev|production]"
  exit 1
fi

echo "Starting web in mode: $MODE"
npm run dev -- --mode "$MODE"