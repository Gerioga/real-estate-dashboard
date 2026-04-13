# Quick Start Guide

## Get it Running in 30 Seconds

### Step 1: Make sure data is in place

```bash
cd "Real estate dashboard"

# Copy data from source (if not already done)
cp -r ../data/dc data/
cp -r ../data/miami data/
cp -r ../data/national data/
```

### Step 2: Run the app

**Easiest way:**
```bash
bash run_local.sh
```

Or **manually**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Step 3: Open in browser

Visit: **http://localhost:8501**

---

## What You'll See

1. **Home Page** — Overview with market selector
2. **Sidebar** — Toggle between "DC Metro" and "Miami-Fort Lauderdale"
3. **Navigation** — 6 analysis pages:
   - Market Overview
   - Price Trends
   - Appreciation
   - Yield Analysis
   - Listing Explorer
   - Investment Calculator

---

## Features

✓ **Multi-market support** — Switch between DC and Miami  
✓ **Corrected tax rates** — Miami uses non-homesteaded 1.15%  
✓ **Dynamic pages** — All content adjusts to selected market  
✓ **Full data** — 21,180+ Miami properties, complete DC metro data  
✓ **Charts & Maps** — Interactive visualizations  
✓ **Investment Calculator** — ROI analysis, break-even yields  

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Data files not found"
```bash
cp -r ../data/dc data/
cp -r ../data/national data/
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Want to deploy online?
See **DEPLOYMENT.md** for GitHub LFS + Streamlit Cloud setup

---

## Data Size

The full dataset is ~205 MB (DC + Miami + National metro data). It's included locally but **not** in the GitHub repo (too large).

For cloud deployment, use GitHub LFS — see DEPLOYMENT.md

---

## That's it! 🚀

Your multi-market real estate investment dashboard is ready to use.

**Questions?** Check:
- README.md — Full documentation
- DATA_SETUP.md — Data file options
- DEPLOYMENT.md — Cloud deployment guide
