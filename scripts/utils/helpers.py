import requests
import os
import json

from timeit import default_timer as timer
from tifffile import TiffFile
from PIL import Image
from PIL.ExifTags import TAGS

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

def get_tif_metadata(image_path: str, metadata_path: str) -> None:
    """Extracts metadata from a TIFF file and saves it to a JSON file.

    Args:
        image_path (str): The path to the TIFF file.
        metadata_path (str): The path to save the extracted metadata JSON file.
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} not found. Pull it from DVC store by running 'dvc pull'.")
        
        print(f"Extracting metadata from {image_path}...")
        metadata = {}
        start_time = timer()

        # Extraction using tifffile
        with TiffFile(image_path) as tif:
            for page in tif.pages:
                for tag in page.tags:
                    metadata[tag.name] = tag.value
        # Extraction using PIL
        with Image.open(image_path) as tif_img_stack:
            # Collect basic image metadata
            metadata["ImageSize"] = tif_img_stack.size
            metadata["Format"] = tif_img_stack.format
            metadata["Mode"] = tif_img_stack.mode
            metadata["Info"] = tif_img_stack.info
            metadata["Frames"] = getattr(tif_img_stack, "n_frames", 1),
            metadata["IsMultiPage"] = getattr(tif_img_stack, "is_multipage", False)
            metadata["IsAnimated"] = getattr(tif_img_stack, "is_animated", False)
            # Get EXIF data
            exifdata = tif_img_stack.getexif()
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = exifdata.get(tag_id)

        end_time = timer()
        print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")
        
        if "error" not in metadata:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            # Save metadata to a JSON file
            json.dump(metadata, open(metadata_path, "w"), indent=4)
            print(f"Metadata extracted and saved to {metadata_path}")
        else:
            print("Error after extracting metadata:", metadata["error"])
    except Exception as e:
        print(f"Error during metadata extraction from {image_path}: {e}")

def extract_all_tif_metadata(filepath, metadata_path: str) -> None:
    """Extracts all available metadata from a TIFF file using tifffile.

    Args:
        filepath (str): The path to the TIFF file.
        metadata_path (str): The path to save the extracted metadata JSON file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found. Pull it from DVC store by running 'dvc pull'.")
        
    print(f"Extracting all available metadata from {filepath}...")
    all_metadata = {}

    start_time = timer()
    try:
        with TiffFile(filepath) as tif:
            # 1. Global TIFF file information (not specific to any page)
            all_metadata['global_info'] = {
                'is_bigtiff': tif.is_bigtiff,
                'is_ome': tif.is_ome,
                'is_lsm': tif.is_lsm, # Example for LSM specific
                'is_fei': tif.is_fei, # Example for FEI specific
                'byteorder': tif.byteorder,
                'series_count': len(tif.series),
                'pages_count': len(tif.pages)
            }

            # 2. OME-XML metadata (if available at the TiffFile level)
            # This is typically the most comprehensive for OME-TIFF
            if tif.ome_metadata is not None:
                all_metadata['ome_xml_global'] = tif.ome_metadata
            else:
                all_metadata['ome_xml_global'] = "No OME-XML metadata found at global level."

            # 3. Proprietary metadata (LSM, FEI, STK, etc.)
            # These attributes only exist if the file is of that specific type
            if tif.is_lsm:
                all_metadata['lsm_metadata'] = tif.lsm_metadata
            if tif.is_fei:
                all_metadata['fei_metadata'] = tif.fei_metadata

            # 4. Metadata for each individual TIFF page/IFD
            all_metadata['pages'] = []
            for i, page in enumerate(tif.pages):
                page_data = {
                    'page_index': i,
                    'shape': page.shape,
                    'dtype': str(page.dtype),
                    'is_tiled': page.is_tiled,
                    'compression': page.compression,
                    'photometric': page.photometric,
                    'resolution': page.resolution,
                    'resolution_unit': page.resolutionunit,
                    'x_resolution': page.x_resolution,
                    'y_resolution': page.y_resolution,
                    'is_contiguous': page.is_contiguous,
                    'is_subsampled': page.is_subsampled,
                    'image_description': page.image_description, # Raw ImageDescription tag string
                    # Raw TIFF tags for the current page
                    'tiff_tags': {}
                }

                for tag in page.tags.values():
                    try:
                        # Attempt to get a more structured representation if available
                        if hasattr(tag, 'value'):
                            tag_value = tag.value
                        elif hasattr(tag, 'asarray'): # For array-like tags
                            tag_value = tag.asarray().tolist()
                        else:
                            tag_value = repr(tag) # Fallback to representation

                        page_data['tiff_tags'][tag.name] = tag_value
                    except Exception as e:
                        page_data['tiff_tags'][tag.name] = f"Error reading tag: {e}"

                # OME-XML metadata specific to this page (if it's an OME-TIFF page)
                if page.ome_metadata is not None:
                    page_data['ome_xml_page'] = page.ome_metadata
                else:
                    page_data['ome_xml_page'] = "No OME-XML metadata specific to this page."

                all_metadata['pages'].append(page_data)

        end_time = timer()
        print(f"All metadata extraction completed in {(end_time - start_time):.2f} seconds.")

        # Save all metadata to a JSON file
        if "error" not in all_metadata:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            # Save metadata to a JSON file
            json.dump(all_metadata, open(metadata_path, "w"), indent=4)
            print(f"All metadata extracted and saved to {metadata_path}")
        else:
            print("Error after extracting all metadata:", all_metadata["error"])

    except Exception as e:
        print(f"Error reading TIFF file {filepath}: {e}")