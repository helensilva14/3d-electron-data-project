import ftplib
import sys
import os

from utils.helpers import download_ftp_files
from timeit import default_timer as timer
from utils.metadata import extract_dm3_metadata

FTP_HOST = "ftp.ebi.ac.uk"
FTP_PATH = "/empiar/world_availability/11759/data/"
SAVE_PATH = "data/raw/empiar_11759_dataset"

METADATA_FOLDER = "outputs/empiar_11759_metadata"

def download_dataset():
    """Downloads the EMPIAR 11759 (Developing retina in zebrafish 55 hpf larval eye) dataset."""
    if os.path.exists(SAVE_PATH):
        print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
    else:
        print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
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
    """Extracts metadata from the downloaded DM3 files in the dataset."""
    if os.path.exists(METADATA_FOLDER):
        print(f"Metadata folder already exists at {METADATA_FOLDER}. Skipping extraction.")
    else:
        print(f"Metadata folder not found at {METADATA_FOLDER}. Proceeding with extraction...")
        os.makedirs(METADATA_FOLDER, exist_ok=True)
        start_time = timer()

        for root, _, files in os.walk(SAVE_PATH):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                extract_dm3_metadata(file_path, METADATA_FOLDER)
        
        end_time = timer()
        print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()