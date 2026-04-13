import streamlit as st
from pathlib import Path
from market_config import get_market_config, list_markets, zip_jurisdiction_dc, zip_jurisdiction_miami

# ── Data directory (relative to project root) ──
BASE = Path(__file__).resolve().parent.parent
DATA_DC = BASE / "data" / "dc"
DATA_NAT = BASE / "data" / "national"
UNIT_DIR = BASE / "output" / "Unit Data"

st.set_page_config(
    page_title="Real Estate Investment Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Market Selection in Sidebar ──
st.sidebar.markdown("## Market Selection")
market = st.sidebar.radio(
    "Choose a market:",
    options=list_markets(),
    index=0,
    horizontal=False
)

# Get market config
market_config = get_market_config(market)

# ── Shared colour palette ──
PTYPE_COLORS = {
    "Condo/Co-op": "#0071BC",
    "Townhouse": "#EC553A",
    "Single Family Residential": "#4CBB88",
    "Multi-Family (2-4 Unit)": "#862C8E",
}

# Store market and paths in session for pages to access
st.session_state["MARKET"] = market
st.session_state["MARKET_CONFIG"] = market_config
st.session_state["DATA_DC"] = DATA_DC
st.session_state["DATA_NAT"] = DATA_NAT
st.session_state["UNIT_DIR"] = UNIT_DIR
st.session_state["JURIS_COLORS"] = market_config["colors"]
st.session_state["PTYPE_COLORS"] = PTYPE_COLORS

# ── Landing page ──
emoji_map = {"DC Metro": "🏛️", "Miami-Fort Lauderdale": "🌴"}
emoji = emoji_map.get(market, "🏠")

color_map = {"DC Metro": "#002245", "Miami-Fort Lauderdale": "#FF6F00"}
accent_color = color_map.get(market, "#0071BC")

st.markdown(
    f"""
    <div style="text-align:center; padding: 40px 20px;">
        <h1 style="color:{accent_color}; font-size:2.6rem;">{emoji} {market_config['name']}</h1>
        <p style="font-size:1.2rem; color:#555;">
            Real Estate Investment Dashboard
        </p>
        <hr style="width:60%; margin:20px auto; border-color:{accent_color};">
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Aggregated Analysis")
    st.markdown(
        "- **Market Overview** — headline metrics & choropleth map\n"
        "- **Price Trends** — time-series by area & property type\n"
        "- **Appreciation** — Zillow ZHVI historical trends\n"
        "- **Yield Analysis** — investment yield rankings"
    )
with col2:
    st.markdown("### Listing Data")
    st.markdown(
        "- **Listing Explorer** — browse individual Redfin listings\n"
        "- Filter by area, type, beds, price range\n"
        "- Interactive map & detail table"
    )
with col3:
    st.markdown("### Investment Tools")
    st.markdown(
        "- **Investment Calculator** — mortgage, equity & true cost\n"
        "- Break-even analysis vs renting\n"
        "- Nominal vs inflation-adjusted projections"
    )

st.markdown("---")

# ── Market-specific info ──
if market == "DC Metro":
    st.markdown("### Market Info (DC Metro)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Property Tax", "0.85-1.07%")
    with col2:
        st.metric("Avg Insurance", "$1,300/yr")
    with col3:
        st.metric("Avg HOA", "$450/mo")
elif market == "Miami-Fort Lauderdale":
    st.markdown("### Market Info (Miami-Fort Lauderdale)")
    st.warning("⚠️ **NON-HOMESTEADED TAX RATES** — Investment properties do NOT qualify for homestead exemption")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Miami-Dade Tax", "1.15%")
    with col2:
        st.metric("Avg Insurance", "$2,750/yr*")
        st.caption("*0.55% of property value (2.3x national avg)")
    with col3:
        st.metric("Avg HOA", "$300/mo")

st.markdown("---")

# ── Databases ──
st.markdown("## Data Sources")

if market == "DC Metro":
    st.markdown(
        """
| Database | File | Description |
|---|---|---|
| **Redfin Market Tracker** | `dc_arl_alex.tsv` | Quarterly zip-level aggregates: median sale price, $/sqft, days on market, sale-to-list ratio, homes sold, YoY changes. Covers DC, Arlington & Alexandria zip codes (2012–present). |
| **Zillow ZHVI** | `zhvi_condo.csv` | Zillow Home Value Index for condos by zip code and neighborhood. Annual values 2000–2026, used for long-term appreciation analysis. |
| **HUD Fair Market Rents** | `hud_fmr_2025.csv` | FY 2025 Fair Market Rents by zip code and bedroom count (0BR–4BR). Published by HUD, used as rent estimate for yield calculations. |
| **Yield Analysis** | `yield_analysis.csv` | Pre-computed median price, sqft, and gross yield by zip / property type / bedroom count, derived from Redfin + HUD FMR. |
| **Redfin Listings** | `redfin_*_new.csv` | Individual active listings scraped from Redfin for DC, Arlington, Alexandria & Richmond. Includes address, price, beds, baths, sqft, HOA, coordinates. |
| **GeoJSON** | `dc_zcta.geojson` | Zip Code Tabulation Area boundaries for the DC metro, used for choropleth maps. |
"""
    )
elif market == "Miami-Fort Lauderdale":
    st.markdown(
        """
| Database | File | Description |
|---|---|---|
| **Redfin Market Tracker** | `new_metros.tsv` | National quarterly zip-level aggregates for 21,180+ properties across 83 Miami-Dade & Broward County zips (2012–present). |
| **HUD Fair Market Rents** | `hud_fmr_new_metros.csv` | FY 2025 Fair Market Rents for Miami-Dade and Broward areas by zip code and bedroom count. |
| **Market Analysis** | Miami analysis CSVs | Corrected analysis with non-homesteaded tax rates (1.15% Miami-Dade, 0.85% Broward) and insurance costs (0.55% annually). |
| **GeoJSON** | `miami_zcta.geojson` | Zip Code Tabulation Area boundaries for Miami-Dade & Broward County, used for choropleth maps. |
"""
    )

st.markdown("---")

# ── Glossary ──
st.markdown("## Glossary")
st.markdown(
    """
| Term | Definition |
|---|---|
| **Median Sale Price** | The middle value of all closed sale prices in a zip code for a given period. |
| **$/sqft (PPSF)** | Price per square foot — sale price divided by living area. Allows comparison across different-sized units. |
| **Days on Market (DOM)** | Number of days from listing to accepted offer. Lower = hotter market. |
| **Sale-to-List Ratio** | Final sale price divided by original list price. >1.0 means homes sell above asking. |
| **YoY Change** | Year-over-year percentage change in median sale price compared to the same period last year. |
| **ZHVI** | Zillow Home Value Index — Zillow's smoothed, seasonally adjusted estimate of the typical home value in an area. |
| **HUD FMR** | Fair Market Rent — HUD's estimate of the 40th-percentile rent (including utilities) for a given area and bedroom count. Used as a conservative rent proxy. |
| **Gross Yield** | Annual rent / purchase price. Does not account for expenses. |
| **Net Yield** | (Annual rent - HOA - property tax - 1% maintenance) / purchase price. A simple pre-financing return estimate. |
| **Price-to-Rent Ratio** | Purchase price / annual rent. Lower = better for investors. Under 15 is generally favorable. |
| **Monthly Cash Flow** | Net operating income / 12. Positive = the property covers its costs from rent alone (pre-mortgage). |
| **HOA** | Homeowners Association monthly fee. Covers building maintenance, amenities, insurance, reserves. |
| **Property Tax** | Annual tax assessed by the local jurisdiction, expressed as a rate of assessed value (varies by city/county). |
| **Opportunity Cost** | The return you forgo by tying up your down payment in real estate instead of investing it (e.g. in the S&P 500). |
| **Real (inflation-adjusted)** | Values deflated by an assumed inflation rate to show purchasing-power-equivalent dollars. |
"""
)

st.caption("Use the sidebar to navigate between pages.")
