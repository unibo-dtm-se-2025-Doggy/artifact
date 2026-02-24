#!/bin/bash
set -e

echo "🔍 Running web checks..."

npm ci
npm run lint
npm run build

echo "✅ All checks passed!"