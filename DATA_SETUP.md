# Data Setup Guide

The Real Estate Investment Dashboard requires data files that are too large for GitHub. You need to set them up locally or on Streamlit Cloud.

---

## Local Development Setup

### Copy data from source directory

```bash
# Navigate to dashboard
cd "Real estate dashboard"

# Copy data files from your local Dropbox location
cp -r ../data/dc data/
cp -r ../data/miami data/
cp -r ../data/national data/

# Verify structure
ls -la data/
# Should show: dc/, miami/, national/
```

### Required Files

#### DC Metro (`data/dc/`)
- `dc_arl_alex.tsv` — Redfin quarterly aggregates (69MB)
- `hud_fmr_2025.csv` — HUD Fair Market Rents
- `zhvi_condo.csv` — Zillow Home Value Index
- `dc_zcta.geojson` — Zip code boundaries

#### Miami-Fort Lauderdale (`data/miami/`)
- `miami_zcta.geojson` — Zip code boundaries

#### National Data (`data/national/`)
- `new_metros.tsv` — Redfin national data (filtered for Miami/Chicago/etc)
- `hud_fmr_new_metros.csv` — HUD FMR for national metros
- `zhvi_all_metros.csv` — Zillow ZHVI national

---

## Streamlit Cloud Deployment

Streamlit Cloud doesn't include large data files. You have two options:

### Option A: Upload Data to Streamlit Cloud Secrets (Easy, Limited)

Works only if data is <50MB total:

1. Go to your Streamlit Cloud app → Manage app
2. Settings → Secrets
3. Upload/paste data files
4. Add to app code:
   ```python
   import streamlit as st
   # Access from secrets if needed
   ```

**Problem**: Data files are >156MB, too large for this approach

### Option B: Use Cloud Storage (Recommended)

Store data in cloud storage and fetch at runtime:

**Option B.1: GitHub LFS (Large File Storage)**
```bash
# Install git-lfs
brew install git-lfs

# Track large files
git lfs track "data/**/*.tsv"
git lfs track "data/**/*.csv"

# Commit and push
git add .gitattributes data/
git commit -m "Add data files via LFS"
git push
```

Then Streamlit Cloud auto-fetches from LFS.

**Option B.2: AWS S3 / Google Cloud Storage**
```python
# In app.py or pages, fetch from cloud:
import pandas as pd
import s3fs

fs = s3fs.S3FileSystem()
df = pd.read_csv('s3://your-bucket/dc_arl_alex.tsv', sep='\t')
```

**Option B.3: Dropbox / Google Drive**
```python
# Fetch from public Dropbox link
url = 'https://dl.dropboxusercontent.com/s/xxx/dc_arl_alex.tsv?dl=1'
df = pd.read_csv(url, sep='\t')
```

---

## Quick Local Setup (For Testing)

If you just want to test locally:

```bash
cd "Real estate dashboard"

# Copy minimal data to test
cp -r ../data/dc data/
cp ../data/national/hud_fmr_2025.csv data/dc/  # If needed

# Run app
streamlit run app.py
```

---

## Testing if Data is Found

Run this in the dashboard directory:

```bash
python3 << 'EOF'
from pathlib import Path

BASE = Path('.')
files_to_check = [
    'data/dc/dc_arl_alex.tsv',
    'data/dc/hud_fmr_2025.csv',
    'data/dc/zhvi_condo.csv',
    'data/dc/dc_zcta.geojson',
    'data/miami/miami_zcta.geojson',
    'data/national/new_metros.tsv',
    'data/national/hud_fmr_new_metros.csv',
]

for f in files_to_check:
    exists = (BASE / f).exists()
    status = '✓' if exists else '✗'
    print(f"{status} {f}")
EOF
```

---

## Recommended: GitHub LFS + Streamlit Cloud

This is the easiest for cloud deployment:

1. **Install git-lfs** (one-time)
   ```bash
   brew install git-lfs
   ```

2. **Track large files**
   ```bash
   cd "Real estate dashboard"
   git lfs install
   git lfs track "*.tsv" "*.csv"
   git add .gitattributes
   ```

3. **Add data files**
   ```bash
   git add data/
   git commit -m "Add data files via LFS"
   git push origin main
   ```

4. **Streamlit Cloud** automatically downloads from LFS when deploying

---

## Alternative: Skip Data Visualization

If you want to get the app running quickly without data:

1. Comment out pages that require data:
   - `pages/2_Price_Trends.py`
   - `pages/4_Yield_Analysis.py`
   - `pages/5_Listing_Explorer.py`

2. Keep these pages (no data needed):
   - `pages/1_Market_Overview.py` (description only)
   - `pages/3_Appreciation.py` (static example)
   - `pages/6_Investment_Calculator.py` (calculator only)

---

## Summary

| Setup | Effort | Cost | Best For |
|---|---|---|---|
| **Copy locally** | 2 min | Free | Local development |
| **GitHub LFS** | 5 min | Free | Cloud + GitHub |
| **AWS S3** | 15 min | $0-1/mo | Large-scale, CDN |
| **Streamlit Cloud Secrets** | 5 min | Free | Small data only (<50MB) |

**Recommended for Streamlit Cloud**: GitHub LFS (easiest, no extra setup)

---

## Questions?

- **Data too large**: Use GitHub LFS (tracks files, doesn't store in repo)
- **Want to skip data**: Comment out data-dependent pages
- **Need live updates**: Use cloud storage + fetch at runtime
- **Local only**: Just copy data/ folder from Dropbox

Choose your approach and let me know if you hit issues!
