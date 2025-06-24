DATASET_URL = "gs://neuroglancer-janelia-flyem-hemibrain/v1.0/segmentation"
SAVE_PATH = "data/raw/hemibrain_ng.gz"
METADATA_FILE = "outputs/hemibrain_ng_metadata.json"
ALL_METADATA_FILE = "outputs/hemibrain_ng_all_metadata.json"

def download_dataset():
    """Downloads the Hemibrain Neuroglancer dataset."""
    pass

def extract_metadata():
    """Extracts metadata from the downloaded file and saves it to a JSON file."""
    pass

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()