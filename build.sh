#!/usr/bin/env bash
# Rebuild the site and write it to the SERVED filenames at the repo root.
set -e
cd "$(dirname "$0")"
python3 build_bible.py
python3 build_chart.py
cp KJV_Rightly_Divided.html ../index.html
cp KJV_Division_Companion_Chart.html ../chart.html
echo "Built -> ../index.html and ../chart.html. Commit and push to redeploy."
