import os
import quilt3 as q3

from timeit import default_timer as timer
from utils.metadata import extract_zarr_metadata

BUCKET_ROOT = "s3://janelia-cosem-datasets"
BUCKET_PATH = "jrc_mus-nacc-2/jrc_mus-nacc-2.zarr/recon-2/em/fibsem-int16/"

SAVE_PATH = "data/raw/jrc_mus_nacc_2.zarr/"
METADATA_FILE = "outputs/jrc_mus_nacc_zarr_metadata.json"

def download_dataset():
    """Downloads the Janelia Mouse nucleus accumbens (JRC-MUS-NACC) dataset."""
    if os.path.exists(SAVE_PATH):
        print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
    else:
        print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
        os.makedirs(SAVE_PATH, exist_ok=True)
        start_time = timer()

        try:
            bucket = q3.Bucket(BUCKET_ROOT)
            # Download the Zarr container from the specified path in the S3 bucket
            bucket.fetch(BUCKET_PATH, SAVE_PATH)
        except Exception as e:
            print(f"\nError downloading {BUCKET_ROOT}/{BUCKET_PATH}: {e}")

        end_time = timer()
        print(f"Download completed in {(end_time - start_time):.2f} seconds.")

def extract_metadata():
    """Extracts metadata from the downloaded Zarr container and saves it to a JSON file."""
    extract_zarr_metadata(SAVE_PATH, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()