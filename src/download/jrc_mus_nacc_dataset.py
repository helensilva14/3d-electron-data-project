import quilt3 as q3

BUCKET_ROOT = "s3://janelia-cosem-datasets"
INTERNAL_PATH = "jrc_mus-nacc-2/jrc_mus-nacc-2.zarr/recon-2/em/fibsem-int16/"
SAVE_PATH = "data/raw/jrc_mus_nacc_2.zarr/"

METADATA_FILE = "outputs/jrc_mus_nacc_2_metadata.json"
ALL_METADATA_FILE = "outputs/jrc_mus_nacc_2_all_metadata.json"

def download_dataset():
    """Downloads the Janelia Mouse nucleus accumbens dataset."""
    bucket = q3.Bucket(BUCKET_ROOT)
    bucket.fetch(INTERNAL_PATH, SAVE_PATH)

def extract_metadata():
    """Extracts metadata from the downloaded Zarr file and saves it to a JSON file."""
    pass

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()