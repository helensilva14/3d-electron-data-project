import requests

from PIL import Image
from PIL.ExifTags import TAGS

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

def get_tif_metadata(image_path):
    """
    Retrieves metadata from a TIFF image.

    Args:
        image_path (str): The path to the TIFF image file.

    Returns:
        dict: A dictionary containing the image metadata.
    """
    try:
        image = Image.open(image_path)
        metadata = {
            # Extract basic metadata
            "basic_info": {
                "Image Size": image.size,
                "Image Height": image.height,
                "Image Width": image.width,
                "Image Format": image.format,
                "Image Mode": image.mode,
                "Image is Animated": getattr(image, "is_animated", False),
                "Frames in Image": getattr(image, "n_frames", 1),
            }
        }
        # Extract EXIF data
        exifdata = image.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = exifdata.get(tag_id)
        return metadata
    
    except FileNotFoundError:
        return {"error": "File not found."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}