#!/bin/bash

# Real Estate Dashboard - Local Setup Script
# Run this to set up and launch the dashboard locally

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  Real Estate Investment Dashboard - Local Setup"
echo "════════════════════════════════════════════════════════════════"

# Check if data exists
echo ""
echo "1️⃣  Checking data files..."

REQUIRED_FILES=(
    "data/dc/dc_arl_alex.tsv"
    "data/dc/hud_fmr_2025.csv"
    "data/dc/zhvi_condo.csv"
    "data/dc/dc_zcta.geojson"
    "data/miami/miami_zcta.geojson"
    "data/national/new_metros.tsv"
    "data/national/hud_fmr_new_metros.csv"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file (MISSING)"
        MISSING=$((MISSING+1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo ""
    echo "⚠️  Some data files are missing!"
    echo ""
    echo "   To fix, copy data from the parent directory:"
    echo "   $ cp -r ../data/dc data/"
    echo "   $ cp -r ../data/national data/"
    echo "   $ cp -r ../data/miami data/"
    echo ""
    exit 1
fi

echo ""
echo "✓ All data files found!"

# Create virtual environment if needed
echo ""
echo "2️⃣  Setting up Python environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ Created virtual environment"
fi

source venv/bin/activate
echo "   ✓ Virtual environment activated"

# Install requirements
echo ""
echo "3️⃣  Installing dependencies..."
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"

# Launch app
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✓ All set! Launching dashboard..."
echo ""
echo "Visit: http://localhost:8501"
echo "Markets: DC Metro, Miami-Fort Lauderdale"
echo ""
echo "To stop: Press Ctrl+C"
echo "════════════════════════════════════════════════════════════════"
echo ""

streamlit run app.py
