#!/bin/bash

# Setup script for frontend web project

set -e

echo "🌐 Setting up web environment..."

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo ""
    echo "Install Node.js from:"
    echo "https://nodejs.org/"
    echo ""
    echo "Recommended version: 18 or 20"
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    echo "Reinstall Node.js from https://nodejs.org/"
    exit 1
fi

echo "📌 Node version: $(node -v)"
echo "📌 npm version: $(npm -v)"

echo ""
echo "📦 Installing dependencies..."

if [ -f package-lock.json ]; then
    npm ci || npm install
else
    npm install
fi

echo ""
echo "✅ Web setup complete!"
echo ""
echo "Run web server:"
echo "  ./scripts/run.sh local"