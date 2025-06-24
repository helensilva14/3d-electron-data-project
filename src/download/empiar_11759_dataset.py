DATASET_URL = "https://ftp.ebi.ac.uk/empiar/world_availability/11759/data/"
SAVE_PATH = "data/raw/empiar_11759.gz"
METADATA_FILE = "outputs/empiar_11759_metadata.json"
ALL_METADATA_FILE = "outputs/empiar_11759_all_metadata.json"

def download_dataset():
    """Downloads the EMPIAR 11759 (Developing retina in zebrafish 55 hpf larval eye) dataset."""
    pass

def extract_metadata():
    """Extracts metadata from the downloaded Zarr file and saves it to a JSON file."""
    pass

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()