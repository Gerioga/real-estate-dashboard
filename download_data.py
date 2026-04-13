"""
Download data files from GitHub Release on first run.
Used by Streamlit Cloud to fetch data automatically.
"""

import streamlit as st
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
def ensure_data_available():
    """Download all required data files from GitHub Release."""

    # Create directories
    Path("data/dc").mkdir(parents=True, exist_ok=True)
    Path("data/miami").mkdir(parents=True, exist_ok=True)
    Path("data/national").mkdir(parents=True, exist_ok=True)

    # Check which files need to be downloaded
    files_to_download = []
    for local_path in DATA_FILES.keys():
        # Check if final file exists (uncompressed)
        final_path = local_path[:-3] if local_path.endswith('.gz') else local_path
        if not Path(final_path).exists():
            files_to_download.append(local_path)

    if not files_to_download:
        return True

    with st.spinner(f"📥 Downloading {len(files_to_download)} data files..."):
        for local_path in files_to_download:
            url = DATA_FILES[local_path]

            try:
                # Download file
                urllib.request.urlretrieve(url, local_path)

                # Decompress if .gz
                if local_path.endswith('.gz'):
                    output_path = local_path[:-3]  # Remove .gz
                    with gzip.open(local_path, 'rb') as f_in:
                        with open(output_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    Path(local_path).unlink()  # Remove .gz file

            except Exception as e:
                st.error(f"Failed to download {local_path}: {e}")
                return False

    st.success("✓ Data files loaded!")
    return True
