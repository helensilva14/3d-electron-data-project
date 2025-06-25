import requests
import os
import json

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
            print(f"File {save_path} does not exist. Downloading...")
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
            print(f"File {save_path} already exists. Skipping download.")
            return
    except Exception as e:
        print(f"Error downloading {url}: {e}")

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