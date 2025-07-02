import zarr
import os

from cloudvolume import CloudVolume
from timeit import default_timer as timer
from utils.metadata import extract_zarr_metadata

DATASET_URL = "gs://neuroglancer-janelia-flyem-hemibrain/v1.0/segmentation/"

SAVE_PATH = "data/raw/hemibrain_1000x1000x1000_crop.zarr/"
METADATA_FILE = "outputs/hemibrain_ng_zarr_metadata.json"

def download_dataset():
    """Downloads a 1000x1000x1000 pixel crop of the Hemibrain Neuroglancer dataset."""
    if os.path.exists(SAVE_PATH):
        print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
    else:
        print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
        # Defining bounding box (start_coord_xyz, end_coord_xyz) and scale for a 1000x1000x1000 pixel crop region
        start_coords, size_coords = (0, 0, 0), (1000, 1000, 1000)
        end_coords = (start_coords[0] + size_coords[0],
                    start_coords[1] + size_coords[1],
                    start_coords[2] + size_coords[2])
                
        try:
            print(f"Downloading a 1000x1000x1000 crop from {start_coords} to {end_coords}...")
            start_time = timer()

            # CloudVolume will find the 'info' file and data chunks/shards from the base URL
            volume = CloudVolume(cloudpath=DATASET_URL)
            # Download the specified crop region
            full_crop = volume[
                start_coords[0] : end_coords[0],
                start_coords[1] : end_coords[1],
                start_coords[2] : end_coords[2]
            ]
            # Save the downloaded crop to a local Zarr file/directory
            os.makedirs(SAVE_PATH, exist_ok=True)
            zarr.save(SAVE_PATH, full_crop)

            end_time = timer()
            print(f"Download completed in {(end_time - start_time):.2f} seconds.")

        except Exception as e:
            print(f"Error downloading {DATASET_URL}: {e}")
            return None

def extract_metadata():
    """Extracts metadata from the downloaded Zarr container and saves it to a JSON file."""
    extract_zarr_metadata(SAVE_PATH, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()