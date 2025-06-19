import requests

def download_file(url, save_path):
    """
    Downloads a file from a URL and saves it to a specified path.

    Args:
        url (str): The URL of the file.
        save_path (str): The local path to save the downloaded file.
    """
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an error for HTTP errors
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192): # TODO: Adjust chunk size to faster download
                    file.write(chunk)
        print(f"Downloaded {url} to {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
