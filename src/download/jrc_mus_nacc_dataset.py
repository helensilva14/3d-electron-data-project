DATASET_URL = "s3://janelia-cosem-datasets/jrc_mus-nacc-2/jrc_mus-nacc-2.zarr"
SAVE_PATH = "data/raw/jrc_mus_nacc_2.zarr"
METADATA_FILE = "outputs/jrc_mus_nacc_2_metadata.json"
ALL_METADATA_FILE = "outputs/jrc_mus_nacc_2_all_metadata.json"

def download_dataset():
    """Downloads the Janelia Mouse nucleus accumbens dataset."""
    pass

def extract_metadata():
    """Extracts metadata from the downloaded Zarr file and saves it to a JSON file."""
    pass

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()