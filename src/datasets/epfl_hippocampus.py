from utils.helpers import download_file
from utils.metadata import extract_all_tif_metadata

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
SAVE_PATH = "data/raw/epfl_volumedata.tif"
METADATA_FILE = "outputs/epfl_hippocampus_metadata.json"

def download_dataset():
    """Downloads the EPFL Electron Microscopy Hippocampus dataset."""
    download_file(DATASET_URL, SAVE_PATH)

def extract_metadata():
    """Extracts metadata from the downloaded TIFF file and saves it to a JSON file."""
    extract_all_tif_metadata(SAVE_PATH, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()