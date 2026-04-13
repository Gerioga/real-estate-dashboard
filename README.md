# Real Estate Investment Dashboard

**Multi-Market Edition** — DC Metro + Miami-Fort Lauderdale

---

## What's New

### 🎯 Multi-Market Support

Dashboard now supports **two markets** with a selector in the sidebar:

- **DC Metro** — Washington DC, Arlington, Alexandria, Richmond
  - Tax rates: 0.85-1.07% (homesteaded)
  - Avg insurance: $1,300/yr
  - Avg HOA: $450/mo

- **Miami-Fort Lauderdale** — Miami-Dade & Broward County
  - **Tax rates: 1.15% (Miami-Dade) / 0.85% (Broward)** ⚠️ Non-homesteaded
  - Avg insurance: $2,750/yr (0.55% of value — 2.3x national avg)
  - Avg HOA: $300/mo

### 📊 Dynamic Pages

All 6 analysis pages automatically adjust to selected market:

1. **Market Overview** — Market metrics, jurisdiction colors, choropleth maps
2. **Price Trends** — Time-series by area and property type
3. **Appreciation** — Zillow ZHVI historical trends
4. **Yield Analysis** — Market-specific investment yield rankings
5. **Listing Explorer** — Browse active Redfin listings with filters
6. **Investment Calculator** — Break-even analysis, mortgage scenarios

### ✨ Critical Tax Rate Correction (Miami)

Miami analysis now uses **1.15% non-homesteaded tax rate** (was 0.79% homesteaded):

- **Why**: Homestead exemptions only apply to primary owner-occupied residences
- **Impact**: +$1,600-4,800/year additional costs depending on property price
- **Status**: Reflected in all Miami yield calculations and breakeven analysis

---

## Project Structure

```
Real estate dashboard/
├── app.py                    # Main app (market selector + landing page)
├── market_config.py          # Market configuration (NEW)
├── requirements.txt          # Python dependencies
├── DEPLOYMENT.md             # Deployment guide (NEW)
├── README.md                 # This file
│
├── pages/                    # Streamlit pages (auto-discovered)
│   ├── 1_Market_Overview.py
│   ├── 2_Price_Trends.py
│   ├── 3_Appreciation.py
│   ├── 4_Yield_Analysis.py
│   ├── 5_Listing_Explorer.py
│   └── 6_Investment_Calculator.py
│
├── .streamlit/
│   └── config.toml           # Streamlit config (NEW)
│
└── data/                     # Data files (symlinked from parent)
    ├── dc/                   # DC Metro data
    ├── miami/                # Miami-Fort Lauderdale data
    └── national/             # National Redfin + HUD data
```

---

## Running Locally

### Prerequisites
- Python 3.8+
- `pip` or `conda`

### Installation

```bash
cd "Real estate dashboard"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

### Quick Test

1. Open sidebar → Select "DC Metro" or "Miami-Fort Lauderdale"
2. Go through pages:
   - Market Overview (should show jurisdiction colors for selected market)
   - Price Trends (should show market-specific zip codes)
   - Yield Analysis (should calculate yields with correct tax rates)
   - Listing Explorer (should filter by market zips)
   - Investment Calculator (should use market's tax/insurance rates)

---

## Deployment

**See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.**

### Quick Start: Streamlit Cloud (Recommended)

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo, select `app.py`
4. Click Deploy
5. (Optional) Add Cloudflare DNS CNAME pointing to Streamlit URL

**Time**: ~5 minutes

### Other Options

- **Vercel** — Better integration with Cloudflare DNS
- **Railway / Render** — More control, requires paid tier

---

## Market Configuration (market_config.py)

All market-specific settings are centralized:

```python
MARKETS = {
    "DC Metro": {
        "name": "...",
        "tax_rates": {...},
        "avg_insurance": 1300,
        "colors": {...},
        "zip_labels": {...},
        ...
    },
    "Miami-Fort Lauderdale": {
        "name": "...",
        "tax_rates": {"Miami-Dade": 0.0115, "Broward": 0.0085},
        "avg_insurance": 2750,
        "colors": {...},
        ...
    },
}
```

To **add a new market**:
1. Add entry to `MARKETS` dict in `market_config.py`
2. Add `zip_jurisdiction_*` function
3. Ensure data files exist in `data/` directory
4. Restart app

---

## Key Files Changed / Added

| File | Status | Notes |
|---|---|---|
| `app.py` | Updated | Added market selector, dynamic config |
| `market_config.py` | New | Centralized market settings |
| `.streamlit/config.toml` | New | Streamlit deployment config |
| `DEPLOYMENT.md` | New | Cloud deployment instructions |
| `pages/*.py` | Unchanged | Pages auto-use `st.session_state["MARKET_CONFIG"]` |

---

## Data Sources

### DC Metro
- **Redfin**: `data/dc/dc_arl_alex.tsv` (69MB, 2012-present)
- **Zillow ZHVI**: `data/dc/zhvi_condo.csv`
- **HUD FMR**: `data/dc/hud_fmr_2025.csv`
- **GeoJSON**: `data/dc/dc_zcta.geojson`

### Miami-Fort Lauderdale
- **Redfin**: `data/national/new_metros.tsv` (filtered for zips 330xx-334xx)
- **HUD FMR**: `data/national/hud_fmr_new_metros.csv`
- **GeoJSON**: `data/miami/miami_zcta.geojson`
- **Analysis**: `output/miami_fort_lauderdale/` (corrected tax rates, insurance)

---

## Important Notes

### Miami Tax Rates

⚠️ **Critical**: Miami uses **1.15% non-homesteaded rate** for investment properties:

- **Why**: Homestead exemptions ($50K deduction) only apply to primary residences
- **Public data trap**: Most Florida tax data shows 0.79% (homesteaded) — this is WRONG for rentals
- **Result**: All Miami yields calculated correctly now (previous estimates were 50%+ too high)

### Cloudflare + Cloudflare Pages

Cloudflare Pages is for **static sites only** (HTML/CSS/JS). Streamlit is a **dynamic Python app**, so:

✗ Cannot deploy directly to Cloudflare Pages
✓ Can use Cloudflare DNS to point to Streamlit Cloud / Vercel / Railway
✓ Can use Cloudflare as reverse proxy (advanced)

Recommended: Deploy to **Streamlit Cloud** or **Vercel**, use **Cloudflare DNS** for custom domain.

---

## Performance

Typical load times:

- **Market Overview**: 1-2 sec (choropleth rendering)
- **Price Trends**: 1-2 sec (multi-series charts)
- **Appreciation**: <1 sec (simple line charts)
- **Yield Analysis**: 2-3 sec (data aggregation)
- **Listing Explorer**: 2-5 sec (depends on filter)
- **Investment Calculator**: <1 sec (arithmetic only)

**Optimization**: Data is cached with `@st.cache_data` decorator. First load is slower, subsequent loads are instant.

---

## Troubleshooting

### Module Import Error
```
ModuleNotFoundError: No module named 'market_config'
```
**Fix**: Ensure `market_config.py` is in same directory as `app.py`

### Data Not Loading
```
FileNotFoundError: 'data/miami/miami_zcta.geojson'
```
**Fix**: Verify data files exist in correct paths relative to app.py

### Pages Not Showing Market Selector
```
KeyError: 'MARKET_CONFIG'
```
**Fix**: Make sure pages are using `st.session_state["MARKET_CONFIG"]` not hardcoded configs

---

## Future Enhancements

- [ ] Add more markets (Tampa, Jacksonville, Atlanta)
- [ ] Integrate property-level risk scoring (flood, heat, etc.)
- [ ] Add mortgage calculator with different loan scenarios
- [ ] Export analysis to PDF/Excel
- [ ] Real-time Redfin scraping (currently uses snapshots)
- [ ] User accounts + saved favorites/portfolios

---

## License

Internal use only — Ruggero's real estate analysis

---

## Contact

For questions or improvements, see parent directory README or DEPLOYMENT.md for support resources.

---

**Last Updated**: April 13, 2026  
**Dashboard Version**: 2.0 (Multi-Market, Corrected Tax Rates)  
**Ready for**: Local testing and cloud deployment
