import ftplib
import sys

from utils.helpers import download_ftp_files

FTP_HOST = "ftp.ebi.ac.uk"
FTP_PATH = "/empiar/world_availability/11759/data/"
SAVE_PATH = "data/raw/empiar_11759_dataset"

METADATA_FILE = "outputs/empiar_11759_metadata.json"
ALL_METADATA_FILE = "outputs/empiar_11759_all_metadata.json"

def download_dataset():
    """Downloads the EMPIAR 11759 (Developing retina in zebrafish 55 hpf larval eye) dataset."""
    try:
        with ftplib.FTP(FTP_HOST) as ftp:
            print(f"\nConnected to FTP server: {FTP_HOST}")
            ftp.login() # No username/password needed for anonymous login for public FTPs
            ftp.encoding = "utf-8" # Ensure correct encoding for filenames
            download_ftp_files(ftp, FTP_PATH, SAVE_PATH)

    except ftplib.all_errors as e:
        print(f"FTP Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def extract_metadata():
    """Extracts metadata from the downloaded Zarr file and saves it to a JSON file."""
    pass

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()