import zarr
import os

from cloudvolume import CloudVolume
from utils.metadata import get_volume_info_metadata

DATASET_URL = "gs://neuroglancer-janelia-flyem-hemibrain/v1.0/segmentation/"
SAVE_PATH = "data/raw/hemibrain_1000x1000x1000_crop.zarr"
METADATA_FILE = "outputs/hemibrain_ng_metadata.json"
ALL_METADATA_FILE = "outputs/hemibrain_ng_all_metadata.json"

def download_dataset() -> object:
    """Downloads the Hemibrain Neuroglancer dataset."""
    if os.path.exists(SAVE_PATH):
        print(f"Dataset already exists at {SAVE_PATH}. Skipping download.")
        return None
    else:
        print(f"Dataset not found at {SAVE_PATH}. Proceeding with download...")
        # For the specified 1000x1000x1000 pixel crop region:
        # You need to define the bounding box (start_coord_xyz, end_coord_xyz) and the scale.
        # Let's assume you want a crop starting at (0,0,0) for simplicity.
        # In a real scenario, you'd specify the exact coordinates for a "random" 1000x1000x1000 crop.
        start_coords, size_coords = (0, 0, 0), (1000, 1000, 1000)
        end_coords = (start_coords[0] + size_coords[0],
                    start_coords[1] + size_coords[1],
                    start_coords[2] + size_coords[2])

        # 2. Initialize CloudVolume: it will find the 'info' file and data chunks/shards from this base URL
        vol = CloudVolume(
            cloudpath=DATASET_URL,
            progress=True, # Show progress bar during download
        )

        try:
            # 4. To download the specific 1000x1000x1000 pixel crop region:
            print(f"\nAttempting to download the 1000x1000x1000 crop from {start_coords} to {end_coords}...")
            # For large downloads, it's good to iterate over sub-chunks or manage memory.
            # CloudVolume handles this fairly well for large regions.
            # The `astype` argument can convert the data type if desired.
            # You might want to save this to a file (e.g., Zarr or HDF5)
            full_crop = vol[
                start_coords[0] : end_coords[0],
                start_coords[1] : end_coords[1],
                start_coords[2] : end_coords[2]
            ]
            print(f"Downloaded 1000x1000x1000 crop with shape: {full_crop.shape} and dtype: {full_crop.dtype}")

            # Save the downloaded crop to a local Zarr file
            zarr.save(SAVE_PATH, full_crop)
            print(f"Saved the 1000x1000x1000 crop to {SAVE_PATH}")

            return vol.info

        except Exception as e:
            print(f"An error occurred while reading the Neuroglancer volume: {e}")
            print("Ensure you have network access and the URL is correct. For very large datasets, sometimes timeouts can occur.")

def extract_metadata(volume_info):
    """Extracts metadata from the downloaded file and saves it to a JSON file."""
    get_volume_info_metadata(volume_info, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    volume_info = download_dataset()
    extract_metadata(volume_info)