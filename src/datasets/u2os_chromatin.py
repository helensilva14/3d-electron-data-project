import ftplib
import sys
import os
import fnmatch

from timeit import default_timer as timer
from utils.metadata import extract_all_tif_metadata

FTP_HOST = "ftp.ebi.ac.uk"
FTP_PATH = "/pub/databases/IDR/idr0086-miron-micrographs/20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed"
FTP_FILE_PATTERN = "Figure_S3B_FIB-SEM_U2OS_*.tif"

SAVE_PATH = "data/raw/u2os_chromatin"
METADATA_FOLDER = "outputs/u2os_chromatin_metadata"

def download_dataset():
    """Downloads the U2OS Chromatin dataset images and saves them as TIFF files."""
    if os.path.exists(SAVE_PATH):
        print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
    else:
        print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
        os.makedirs(SAVE_PATH, exist_ok=True)
        start_time = timer()

        try:
            with ftplib.FTP(FTP_HOST) as ftp:
                print(f"Connected to FTP server: {FTP_HOST}")
                ftp.login() # No username/password needed for anonymous login for public FTPs
                ftp.encoding = "utf-8" # Ensure correct encoding for filenames
                # Change directory within the FTP server
                ftp.cwd(FTP_PATH)

                # Filter files based on the pattern
                matching_files = fnmatch.filter(ftp.nlst(), FTP_FILE_PATTERN)
                for filename in matching_files:
                    local_filepath = os.path.join(SAVE_PATH, filename)
                    with open(local_filepath, "wb") as local_file:
                        ftp.retrbinary(f"RETR {filename}", local_file.write)

        except ftplib.all_errors as e:
            print(f"FTP Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

        end_time = timer()
        print(f"Download completed in {(end_time - start_time):.2f} seconds.")

def extract_metadata():
    """Extracts metadata from the downloaded TIFF files in the dataset."""
    if os.path.exists(METADATA_FOLDER):
        print(f"Metadata folder already exists at {METADATA_FOLDER}. Skipping extraction.")
    else:
        print(f"Metadata folder not found at {METADATA_FOLDER}. Proceeding with extraction...")
        os.makedirs(METADATA_FOLDER, exist_ok=True)
        start_time = timer()

        for root, _, files in os.walk(SAVE_PATH):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                filename_only = os.path.splitext(file_path)[0] # Remove extension

                metadata_file_name = os.path.join(METADATA_FOLDER, f"{filename_only}_metadata.json")
                extract_all_tif_metadata(file_path, metadata_file_name)
        
        end_time = timer()
        print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()