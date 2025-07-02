import os
import dm3_lib
import sys
import numpy as np

from timeit import default_timer as timer
from tifffile import TiffFile
from collections import defaultdict

from utils.helpers import save_metadata_as_json

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
        if filepath.endswith('.dm3'):
            # Use pyDM3reader (dm3_lib) to read the DM3 file
            dm3_file = dm3_lib.DM3(filepath)

            # Get easily accessible metadata
            metadata = {
                "filename": dm3_file.filename,
                "file_version": dm3_file.file_version,
                "image_summary": {
                    "size": dm3_file.size,
                    "dtype": dm3_file.data_type_str if dm3_file.data_type_str else None,
                    "pixel_size_value": dm3_file.pxsize[0] if dm3_file.pxsize else None,
                    "pixel_size_unit": dm3_file.pxsize[1] if dm3_file.pxsize else None,
                    "cuts": dm3_file.cuts
                }
            }

            if dm3_file.tags:
                # Recursively clean and include the entire tag tree
                metadata["full_original_tags"] = _dm3_item_to_json_serializable_recursive(dm3_file.tags)
            
            if dm3_file.info:
                # Recursively clean and include the entire info structure
                metadata["info"] = _dm3_item_to_json_serializable_recursive(dm3_file.info)

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

def _dm3_item_to_json_serializable_recursive(value: object) -> object:
    """ Recursively converts a DM3 item to a JSON-serializable format.
    Handles various data types, including NumPy arrays, bytes, and nested structures.
    
    Args:
        value: The DM3 item to convert to a JSON-serializable format.
    
    Returns:
        A JSON-serializable version of the DM3 item.
    """
    # Convert bytes to a string representation
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    # Skip NumPy arrays to avoid deep recursion and large data serialization
    if isinstance(value, np.ndarray):
        return "Image data (NumPy array) skipped for JSON serialization"
    # Convert NumPy scalar to Python scalar
    elif isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item()
    elif isinstance(value, dict):
        cleaned_dict = {}
        for k, v in value.items():
            if k == 'ImageData' and isinstance(v, np.ndarray):
                 cleaned_dict[k] = "Image data (NumPy array) skipped for JSON serialization"
            else:
                 cleaned_dict[k] = _dm3_item_to_json_serializable_recursive(v)
        return cleaned_dict
    # If the value is a list or tuple, recursively process each item
    elif isinstance(value, (list, tuple)):
        return [_dm3_item_to_json_serializable_recursive(item) for item in value]
    return value

def _find_all_attribute_names(metadata_dict, current_path=""):
    """ Recursively finds all unique attribute names in a nested dictionary structure,
    returning them as a set of strings with their full paths.
    
    Args:
        metadata_dict (dict): The metadata dictionary to search.
        current_path (str): The current path in the nested structure, used for recursion.
    
    Returns:
        A set of unique attribute names with their full paths.
    """
    attribute_names = set()

    if isinstance(metadata_dict, dict):
        for key, value in metadata_dict.items():
            full_path_key = f"{current_path}.{key}" if current_path else key

            if isinstance(value, dict):
                attribute_names.update(
                    _find_all_attribute_names(value, full_path_key)
                )
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    attribute_names.update(
                        _find_all_attribute_names(item, f"{full_path_key}[{i}]")
                    )
            else:
                attribute_names.add(full_path_key)

    return attribute_names

def consolidate_attribute_names(all_metadata_by_filename):
    """Consolidates attribute names from multiple metadata files, identifying those present in multiple datasets.

    Args:
        all_metadata_by_filename (dict): A dictionary mapping filenames to their metadata content.

    Returns:
        dict: A dictionary with consolidated attribute names and their dataset mappings.
    """
    attribute_presence = defaultdict(set) # Maps attribute_name -> set of filenames

    for filename, metadata_content in all_metadata_by_filename.items():
        
        current_dataset_attributes = _find_all_attribute_names(metadata_content)
        for attr_name in current_dataset_attributes:
            attribute_presence[attr_name].add(filename)

    return {
        "attributes_present_in_multiple_datasets": {
            attr: list(files)
            for attr, files in attribute_presence.items()
            if len(files) > 1
        },
        "attributes_unique_to_single_datasets": {
            attr: list(files)
            for attr, files in attribute_presence.items()
            if len(files) == 1
        },
    }