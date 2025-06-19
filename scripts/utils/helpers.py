from urllib.request import urlretrieve

def download_tif_file(url, save_path):
    """
    Downloads a .tif file from a URL and saves it to a specified path.

    Args:
        url (str): The URL of the .tif file.
        save_path (str): The local path to save the downloaded file.
    """
    try:
        urlretrieve(url, save_path)
        print(f"Downloaded {url} to {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
