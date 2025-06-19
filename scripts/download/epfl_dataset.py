import json
import os
from utils.helpers import download_file, get_tif_metadata

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
OUTPUT_PATH = "data/raw/volumedata.tif"
METADATA_FILE = "data/extract/epfl_metadata.json"

def download_epfl():
    """
    Downloads the EPFL Electron Microscopy Hippocampus dataset.
    """
    # TODO: Change to logging statements
    print("Started download of EPFL Electron Microscopy Hippocampus dataset...")

    download_file(DATASET_URL, OUTPUT_PATH)
    # TODO: print elapsed time for download

    print("Finished download of EPFL Electron Microscopy Hippocampus dataset.")

def extract_metadata():
    metadata = get_tif_metadata(OUTPUT_PATH)
    if "error" not in metadata:
        os.makedirs("data/extract", exist_ok=True)
        json.dump(metadata, open(METADATA_FILE, "w"), indent=4)
        print(f"Metadata extracted and saved to {METADATA_FILE}")
    else:
        print("Error:", metadata["error"])