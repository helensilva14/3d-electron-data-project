import json
import os
from utils.helpers import download_file, get_tif_metadata

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
SAVE_PATH = "data/raw/epfl_volumedata.tif"
METADATA_FILE = "outputs/epfl_metadata.json"

def download_epfl():
    """Downloads the EPFL Electron Microscopy Hippocampus dataset."""
    download_file(DATASET_URL, SAVE_PATH)

def extract_metadata():
    """Extracts metadata from the downloaded TIFF file and saves it to a JSON file."""
    print(f"Extracting metadata from {SAVE_PATH}...")
    metadata = get_tif_metadata(SAVE_PATH)

    if "error" not in metadata:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
        # Save metadata to a JSON file
        json.dump(metadata, open(METADATA_FILE, "w"), indent=4)
        print(f"Metadata extracted and saved to {METADATA_FILE}")
    else:
        print("Error extracting metadata:", metadata["error"])