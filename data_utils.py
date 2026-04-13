"""
Data utilities for Real Estate Dashboard
Handles missing data gracefully
"""

import streamlit as st
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

def check_data_file_exists(filename, data_type='csv'):
    """Check if a data file exists."""
    path = BASE / "Real estate dashboard" / filename
    return path.exists()

def missing_data_message(page_name, required_files=None):
    """Display helpful message when data is missing."""
    st.error(
        f"""
        ❌ **Data files not available**

        This page ({page_name}) requires data files that are not in the GitHub repository.

        **To fix:**

        **Option 1: Local Development (Recommended)**
        ```bash
        # Copy data from source
        cp -r ../data/dc data/
        cp -r ../data/national data/
        streamlit run app.py
        ```

        **Option 2: Streamlit Cloud**
        - Use GitHub LFS to store large files
        - See [DATA_SETUP.md](DATA_SETUP.md) for instructions

        **Option 3: Skip to another page**
        - Try the **Investment Calculator** (no data needed)
        """
    )

def safe_load_csv(filepath, **kwargs):
    """
    Safely load CSV with error handling.
    Returns None if file doesn't exist.
    """
    import pandas as pd

    path = BASE / "Real estate dashboard" / filepath

    if not path.exists():
        return None

    try:
        return pd.read_csv(path, **kwargs)
    except Exception as e:
        st.error(f"Error loading {filepath}: {str(e)}")
        return None

def safe_load_geojson(filepath):
    """
    Safely load GeoJSON with error handling.
    Returns None if file doesn't exist.
    """
    import json

    path = BASE / "Real estate dashboard" / filepath

    if not path.exists():
        return None

    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {str(e)}")
        return None

def has_data_for_market(market):
    """Check if data exists for a market."""
    if market == "DC Metro":
        return check_data_file_exists("data/dc/dc_arl_alex.tsv")
    elif market == "Miami-Fort Lauderdale":
        return (check_data_file_exists("data/miami/miami_zcta.geojson") or
                check_data_file_exists("data/national/new_metros.tsv"))
    return False
