from utils.helpers import download_file
from utils.metadata import get_brief_tif_metadata, extract_all_tif_metadata

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
SAVE_PATH = "data/raw/epfl_volumedata.tif"
METADATA_FILE = "data/outputs/epfl_metadata.json"
ALL_METADATA_FILE = "data/outputs/epfl_all_metadata.json"

def download_epfl():
    """Downloads the EPFL Electron Microscopy Hippocampus dataset."""
    download_file(DATASET_URL, SAVE_PATH)

def extract_metadata():
    """Extracts metadata from the downloaded TIFF file and saves it to a JSON file."""
    get_brief_tif_metadata(SAVE_PATH, METADATA_FILE)
    extract_all_tif_metadata(SAVE_PATH, ALL_METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_epfl()
    extract_metadata()