"""
Download data files from GitHub Release on first run.
Used by Streamlit Cloud to fetch data automatically.
"""

import streamlit as st
import os
from pathlib import Path
import urllib.request
import gzip
import shutil

GITHUB_RELEASE_URL = "https://github.com/Gerioga/real-estate-dashboard/releases/download/data-v1"

DATA_FILES = {
    # DC data
    "data/dc/dc_arl_alex.tsv.gz": f"{GITHUB_RELEASE_URL}/dc_arl_alex.tsv.gz",
    "data/dc/hud_fmr_2025.csv": f"{GITHUB_RELEASE_URL}/hud_fmr_2025.csv",
    "data/dc/zhvi_condo.csv": f"{GITHUB_RELEASE_URL}/zhvi_condo.csv",
    "data/dc/dc_zcta.geojson": f"{GITHUB_RELEASE_URL}/dc_zcta.geojson",
    
    # Miami data
    "data/miami/miami_zcta.geojson": f"{GITHUB_RELEASE_URL}/miami_zcta.geojson",
    
    # National data
    "data/national/new_metros.tsv.gz": f"{GITHUB_RELEASE_URL}/new_metros.tsv.gz",
    "data/national/hud_fmr_new_metros.csv": f"{GITHUB_RELEASE_URL}/hud_fmr_new_metros.csv",
}

@st.cache_resource
def download_data_files():
    """Download all required data files from GitHub Release."""
    
    # Create directories
    Path("data/dc").mkdir(parents=True, exist_ok=True)
    Path("data/miami").mkdir(parents=True, exist_ok=True)
    Path("data/national").mkdir(parents=True, exist_ok=True)
    
    for local_path, url in DATA_FILES.items():
        if Path(local_path).exists():
            # File already exists locally
            continue
        
        try:
            print(f"Downloading {local_path}...")
            
            # Download file
            urllib.request.urlretrieve(url, local_path)
            
            # Decompress if .gz
            if local_path.endswith('.gz'):
                output_path = local_path[:-3]  # Remove .gz
                with gzip.open(local_path, 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(local_path)  # Remove .gz file
                print(f"  ✓ {output_path}")
            else:
                print(f"  ✓ {local_path}")
                
        except Exception as e:
            print(f"  ✗ Failed to download {local_path}: {e}")
            return False
    
    return True

def ensure_data_available():
    """Ensure all data files are available (download if needed)."""
    # Check if running on Streamlit Cloud
    is_cloud = os.environ.get('STREAMLIT_SERVER_HEADLESS') == 'true'
    
    if is_cloud:
        # On Streamlit Cloud, download from GitHub Release
        return download_data_files()
    else:
        # Locally, files should already be in place
        return all(Path(f).exists() for f in DATA_FILES.keys() if not f.endswith('.gz'))
