import zarr
import os

from cloudvolume import CloudVolume
from timeit import default_timer as timer
from utils.metadata import get_volume_info_metadata

DATASET_URL = "gs://neuroglancer-janelia-flyem-hemibrain/v1.0/segmentation/"
SAVE_PATH = "data/raw/hemibrain_1000x1000x1000_crop.zarr"

METADATA_FILE = "outputs/hemibrain_ng_metadata.json"
ALL_METADATA_FILE = "outputs/hemibrain_ng_all_metadata.json"

def download_dataset() -> object:
    """Downloads a 1000x1000x1000 pixel crop of the Hemibrain Neuroglancer dataset.

    Returns:
        object: The volume info object containing metadata about the downloaded dataset.
    """
    if os.path.exists(SAVE_PATH):
        print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
        return None
    else:
        print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
        # Defining bounding box (start_coord_xyz, end_coord_xyz) and scale for a 1000x1000x1000 pixel crop region
        start_coords, size_coords = (0, 0, 0), (1000, 1000, 1000)
        end_coords = (start_coords[0] + size_coords[0],
                    start_coords[1] + size_coords[1],
                    start_coords[2] + size_coords[2])
                
        try:
            print(f"\nDownloading a 1000x1000x1000 crop from {start_coords} to {end_coords}...")
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
            zarr.save(SAVE_PATH, full_crop)

            end_time = timer()
            print(f"Download completed in {(end_time - start_time):.2f} seconds.")

            # Return the volume info object containing metadata about the downloaded dataset
            return volume.info

        except Exception as e:
            print(f"Error downloading {DATASET_URL}: {e}")
            return None

def extract_metadata(volume_info: object):
    """Extracts metadata from the downloaded dataset and saves it to a JSON file."""
    get_volume_info_metadata(volume_info, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    volume_info = download_dataset()
    extract_metadata(volume_info)