from utils.helpers import download_file
from utils.metadata import get_brief_tif_metadata, extract_all_tif_metadata

IMAGES_URL = ["https://idr.openmicroscopy.org/webclient/render_image_download/9846137/?format=tif", "https://idr.openmicroscopy.org/webclient/render_image_download/9846133/?format=tif"]
SAVE_PATH = "data/raw/u2os_chromatin.tif"
METADATA_FILE = "outputs/u2os_chromatin_metadata.json"
ALL_METADATA_FILE = "outputs/u2os_chromatin_all_metadata.json"

def download_dataset():
    """Downloads the U2OS Chromatin dataset images and saves them as a TIFF file."""
    for i, url in enumerate(IMAGES_URL):
        download_file(url, f"data/raw/u2os_{i}.tif")
    # TODO: Consolidate downloaded files into a single TIFF file

def extract_metadata():
    """Extracts metadata from the downloaded TIFF file and saves it to a JSON file."""
    get_brief_tif_metadata(SAVE_PATH, METADATA_FILE)
    extract_all_tif_metadata(SAVE_PATH, ALL_METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    # extract_metadata()