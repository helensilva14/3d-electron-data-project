import os
import dm3_lib
import sys
import numpy as np

from timeit import default_timer as timer
from PIL import Image
from PIL.ExifTags import TAGS
from tifffile import TiffFile

from utils.helpers import save_metadata_as_json

def get_brief_tif_metadata(file_path: str, metadata_path: str) -> None:
    """Extracts basic metadata from a TIFF file using PIL (Pillow) and saves it to a JSON file.

    Args:
        file_path (str): The path to the TIFF file.
        metadata_path (str): The path to save the extracted metadata JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found. Pull it from DVC store by running 'dvc pull'.")
    
    if os.path.exists(metadata_path):
        print(f"Metadata file {metadata_path} already exists. Skipping extraction.")
    else:
        print(f"Metadata file {metadata_path} does not exist. Extracting...")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)  
        try:
            metadata = {}
            start_time = timer()
            # Extraction using PIL (Pillow)
            with Image.open(file_path) as tif_img_stack:
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
            
            # Save metadata to a JSON file
            save_metadata_as_json(metadata, metadata_path)
        except Exception as e:
            print(f"Error during metadata extraction from {file_path}: {e}")

def extract_all_tif_metadata(file_path, metadata_path: str) -> None:
    """Extracts all available metadata from a TIFF file using tifffile and saves it to a JSON file.

    Args:
        file_path (str): The path to the TIFF file.
        metadata_path (str): The path to save the extracted metadata JSON file. 
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found. Pull it from DVC store by running 'dvc pull'.")
    
    if os.path.exists(metadata_path):
        print(f"Metadata file {metadata_path} already exists. Skipping extraction.")
    else:
        print(f"Metadata file {metadata_path} does not exist. Extracting...")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True) 
        try:
            print(f"Extracting all available metadata from {file_path}...")
            all_metadata = {}
            start_time = timer()

            # Extraction using tifffile
            with TiffFile(file_path) as tif:
                # 1. Global TIFF file information (not specific to any page)
                all_metadata['global_info'] = {
                    'is_bigtiff': tif.is_bigtiff,
                    'is_ome': tif.is_ome,
                    'is_lsm': tif.is_lsm, 
                    'is_fei': tif.is_fei,
                    'byteorder': tif.byteorder,
                    'series_count': len(tif.series),
                    'pages_count': len(tif.pages)
                }

                # 2. OME-XML metadata (if available at the TiffFile level)
                if hasattr(tif, 'ome_metadata') and tif.ome_metadata is not None:
                    all_metadata['ome_xml_global'] = tif.ome_metadata
                else:
                    all_metadata['ome_xml_global'] = "No OME-XML metadata found at global level."

                # 3. Proprietary metadata (LSM, FEI, STK, etc.)
                if tif.is_lsm:
                    all_metadata['lsm_metadata'] = tif.lsm_metadata
                if tif.is_fei:
                    all_metadata['fei_metadata'] = tif.fei_metadata

                # 4. Metadata for each individual TIFF page/IFD (Image File Directory)
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
                        'is_contiguous': page.is_contiguous,
                        'is_subsampled': page.is_subsampled,
                        'image_description': page.description,
                        # Raw TIFF tags for the current page
                        'page_tiff_tags': {}
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
                            # Store the tag value in the page data
                            page_data['page_tiff_tags'][tag.name] = tag_value
                        except Exception as e:
                            page_data['page_tiff_tags'][tag.name] = f"Error reading tag: {e}"

                    # Add the page data to the global metadata
                    all_metadata['pages'].append(page_data)

            end_time = timer()
            print(f"All metadata extraction completed in {(end_time - start_time):.2f} seconds.")

            # Save all metadata to a JSON file
            save_metadata_as_json(all_metadata, metadata_path)
        except Exception as e:
            print(f"Error reading TIFF file {file_path}: {e}")

def get_volume_info_metadata(volume_info, metadata_path: str) -> None:
    """Extracts metadata from a volume info object and saves it to a JSON file.

    Args:
        volume_info: The volume info object containing metadata.
        metadata_path (str): The path to save the extracted metadata JSON file.
    """
    if os.path.exists(metadata_path):
        print(f"Metadata file {metadata_path} already exists. Skipping extraction.")
    elif volume_info is None:
        print(f"Metadata extraction for a volume info can only be performed at the end of the download process. Skipping extraction.")
    else:
        print(f"Metadata file {metadata_path} does not exist. Extracting...")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)  
        try:
            start_time = timer()
            # Save metadata to a JSON file
            save_metadata_as_json(volume_info, metadata_path)
            end_time = timer()
            print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")
        except Exception as e:
            print(f"Error during metadata extraction from {str(volume_info)}: {e}")

def extract_dm3_metadata(filepath: str, folder_path: str) -> None:
    """
    Extracts all available metadata from a DM3 file using pyDM3reader.

    Args:
        filepath (str): The path to the DM3 file.

    Returns:
        dict: A dictionary containing all extracted metadata.
              Returns None if the file cannot be read or an error occurs.
    """
    try:
        dm3_file = dm3_lib.DM3(filepath) # Use the DM3 class from pyDM3reader

        # Start with common, easily accessible metadata
        metadata = {
            "filename": dm3_file.filename,
            "file_version": dm3_file.file_version,
            "image_summary": { # Summarize image data, not include it
                "size": dm3_file.size,
                "dtype": dm3_file.data_type_str if dm3_file.data_type_str else None,
                "pixel_size_value": dm3_file.pxsize[0] if dm3_file.pxsize else None,
                "pixel_size_unit": dm3_file.pxsize[1] if dm3_file.pxsize else None,
                "cuts": dm3_file.cuts
            }
        }

        if dm3_file.tags:
            # Recursively clean and include the entire tag tree
            metadata["full_original_tags"] = _to_json_serializable_recursive(dm3_file.tags)
        if dm3_file.info:
            # Recursively clean and include the entire info structure
            metadata["info"] = _to_json_serializable_recursive(dm3_file.info)

        # Save metadata to a JSON file
        filename_only = os.path.splitext(os.path.basename(filepath))[0] # Remove extension
        metadata_file_name = os.path.join(folder_path, f"{filename_only}_metadata.json")
        save_metadata_as_json(metadata, metadata_file_name)

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading DM3 file {filepath} with pyDM3reader: {e}", file=sys.stderr)
        return None

def _to_json_serializable_recursive(value):
    if isinstance(value, bytes):
        # Convert bytes to a string representation
        return value.decode('utf-8', errors='ignore')
    if isinstance(value, np.ndarray):
        # Image data array, skip
        return "Image data (NumPy array) skipped for JSON serialization"
    elif isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item() # Convert NumPy scalar to Python scalar
    elif isinstance(value, dict):
        cleaned_dict = {}
        for k, v in value.items():
            # pyDM3reader's internal structure might have keys like 'ImageData'
            # which might hold the actual array. Adapt this check if needed.
            if k == 'ImageData' and isinstance(v, np.ndarray):
                 cleaned_dict[k] = "Image data (NumPy array) skipped for JSON serialization"
            else:
                 cleaned_dict[k] = _to_json_serializable_recursive(v)
        return cleaned_dict
    elif isinstance(value, (list, tuple)):
        return [_to_json_serializable_recursive(item) for item in value]
    return value