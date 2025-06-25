import requests
import os
import json
import ftplib
import sys

from timeit import default_timer as timer

CHUNK_SIZE = 8192  # Default chunk size for downloading files

def download_file(url: str, save_path: str) -> None:
    """Downloads a file from a URL and saves it to a specified path.

    Args:
        url (str): The URL of the file.
        save_path (str): The local path to save the downloaded file.
    """
    try:
        if not os.path.exists(save_path):
            print(f"\nFile {save_path} does not exist. Downloading...")
            print(f"Starting download from {url} to {save_path}...")
            start_time = timer()

            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # Download the file
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  # Raise HTTP errors
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:  # Filter out keep-alive new chunks
                            file.write(chunk)
            
            end_time = timer()
            print(f"Download completed in {(end_time - start_time):.2f} seconds.")
        else:
            print(f"\nFile {save_path} already exists. Skipping download.")
            return
    except Exception as e:
        print(f"\nError downloading {url}: {e}")

def save_metadata_as_json(metadata: dict, save_path: str) -> None:
    """Saves metadata to a JSON file.

    Args:
        metadata (dict): The metadata to save.
        save_path (str): The path to save the metadata JSON file.
    """
    try:
        if "error" not in metadata:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # Save metadata to a JSON file
            with open(save_path, "w") as file:
                json.dump(metadata, file, indent=4)
            print(f"Metadata saved to {save_path}")
        else:
            print(f"Error in obtained metadata: {metadata['error']}")
    except Exception as e:
        print(f"Error saving metadata to {save_path}: {e}")

def download_ftp_files(ftp: ftplib.FTP, remote_path: str, save_path: str) -> None:
    """
    Downloads files from an FTP server using ftp.nlst() exclusively and inferring directory status. 
    It works reliably for older FTP servers that might not support ftp.mlsd(),
    method that returns the file type information (directory or file) directly.

    Args:
        ftp (ftplib.FTP): An authenticated FTP connection object.
        remote_path (str): The path on the FTP server to download from.
        save_path (str): The local directory to save files to.
    """
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        print(f"Error changing directory to {remote_path}: {e}. Skipping download.", file=sys.stderr)
        return

    # Ensure the output directory exists
    os.makedirs(save_path, exist_ok=True)
    items = []
    try:
        items = ftp.nlst()
    except ftplib.error_perm as e:
        print(f"Error listing contents of {remote_path} with nlst(): {e}. Skipping this directory.", file=sys.stderr)
        return
    except Exception as e:
        print(f"An unexpected error occurred while listing {remote_path} with nlst(): {e}. Skipping this directory.", file=sys.stderr)
        return

    print(f"Found {len(items)} items in {remote_path}. Subdirectories will be skipped.")
    print(f"Starting download from {remote_path} to {save_path}...")
    start_time = timer()
    
    for item_name in items:
        try:
            # Try to change directory to see if item is a directory
            ftp.cwd(item_name)
            is_directory = True
            ftp.cwd('..') # Change back immediately if it was a directory
        except ftplib.error_perm:
            # If changing directory fails with a permission error, it's usually a file
            is_directory = False
        except Exception as e:
            print(f"Warning: Could not determine type of '{item_name}' in {remote_path}: {e}. Assuming it's a file.", file=sys.stderr)
            is_directory = False

        local_item_path = os.path.join(save_path, item_name)
        if not is_directory:
            # Download the file only if it does not already exist
            if not os.path.exists(local_item_path):
                try:
                    with open(local_item_path, 'wb') as local_file:
                        ftp.retrbinary(f"RETR {item_name}", local_file.write)
                except Exception as e:
                    print(f"Error downloading {item_name}: {e}", file=sys.stderr)

    end_time = timer()
    print(f"Download completed in {(end_time - start_time):.2f} seconds.")
