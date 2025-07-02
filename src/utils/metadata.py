import os
import dm3_lib
import sys
import numpy as np
import zarr

from timeit import default_timer as timer
from tifffile import TiffFile
from collections import defaultdict

from utils.helpers import save_metadata_as_json

def extract_tif_metadata(file_path: str, metadata_path: str) -> None:
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

def extract_zarr_metadata(file_path: str, metadata_path: str) -> None:
    """Extracts metadata from a Zarr container and saves it to a JSON file.

    Args:
        file_path (str): The path to the Zarr container.
        metadata_path (str): The path to save the extracted metadata JSON file.
    """
    try:
        if os.path.exists(metadata_path):
            print(f"Metadata file {metadata_path} already exists. Skipping extraction.")
        else:
            print(f"Metadata file not found at {metadata_path}. Proceeding with extraction...")
            start_time = timer()
            extracted_metadata = {}
            
            # Load previously downloaded Zarr container
            zarr_content = zarr.open(file_path, mode='r')

            if isinstance(zarr_content, zarr.hierarchy.Group):
                extracted_metadata = __extract_zgroup_metadata_recursive(zarr_content)
            elif isinstance(zarr_content, zarr.core.Array):
                extracted_metadata = __extract_zarray_metadata(zarr_content)
            else:
                raise ValueError("Unknown Zarr object type at root.")

            # Save metadata to a JSON file
            save_metadata_as_json(extracted_metadata, metadata_path)

            end_time = timer()
            print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")

    except Exception as e:
        print(f"\nError extracting metadata from {file_path}: {e}")

def extract_dm3_metadata(file_path: str, folder_path: str) -> None:
    """
    Extracts all available metadata from a DM3 file using pyDM3reader.

    Args:
        filepath (str): The path to the DM3 file.

    Returns:
        dict: A dictionary containing all extracted metadata.
              Returns None if the file cannot be read or an error occurs.
    """
    try:
        if file_path.endswith('.dm3'):
            # Use pyDM3reader (dm3_lib) to read the DM3 file
            dm3_file = dm3_lib.DM3(file_path)

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
                metadata["full_original_tags"] = __convert_to_json_serializable_recursive(dm3_file.tags)
            
            if dm3_file.info:
                # Recursively clean and include the entire info structure
                metadata["info"] = __convert_to_json_serializable_recursive(dm3_file.info)

            # Save metadata to a JSON file
            output_filename = dm3_file.filename.replace(".", "_")
            metadata_file_name = os.path.join(folder_path, f"{output_filename}_metadata.json")
            save_metadata_as_json(metadata, metadata_file_name)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading DM3 file {file_path} with pyDM3reader: {e}", file=sys.stderr)
        return None

def consolidate_attribute_names(all_metadata_by_filename: dict) -> dict:
    """Consolidates attribute names from multiple metadata files, identifying those present in multiple datasets.

    Args:
        all_metadata_by_filename (dict): A dictionary mapping filenames to their metadata content.

    Returns:
        dict: A dictionary with consolidated attribute names and their dataset mappings.
    """
    attribute_presence = defaultdict(set) # Maps attribute_name -> set of filenames

    for filename, metadata_content in all_metadata_by_filename.items():
        
        current_dataset_attributes = _find_all_attribute_names_recursive(metadata_content)
        for attr_name in current_dataset_attributes:
            attribute_presence[attr_name].add(filename)

    return {
        "attributes_present_in_multiple_datasets": [
            attr
            for attr, files in attribute_presence.items()
            if len(files) > 1
        ],
        "attributes_unique_to_single_datasets": {
            filename: f"{len([
                attr for attr, files in attribute_presence.items() if files == {filename}
            ])} unique attributes. Not listed to reduce output size."
            for filename in all_metadata_by_filename.keys()
        },
    }

def __extract_zgroup_metadata_recursive(zgroup: zarr.hierarchy.Group) -> dict:
    """Recursively extracts metadata from a Zarr group, including its attributes and children.

    Args:
        zgroup (zarr.hierarchy.Group): The Zarr group to extract metadata from.

    Returns:
        dict: A dictionary containing the metadata of the Zarr group.
    """
    metadata = {
        "path": zgroup.path,
        "type": "zgroup",
        "attrs": __convert_to_json_serializable_recursive(dict(zgroup.attrs)),
        "children": {}
    }
    for name, item in zgroup.items():
        if isinstance(item, zarr.hierarchy.Group):
            metadata["children"][name] = __extract_zgroup_metadata_recursive(item)
        elif isinstance(item, zarr.core.Array):
            metadata["children"][name] = __extract_zarray_metadata(item)
    return metadata

def __extract_zarray_metadata(zarray: zarr.core.Array) -> dict:
    """Extracts metadata from a Zarr array, including its attributes and properties.

    Args:
        zarray (zarr.core.Array): The Zarr array to extract metadata from.

    Returns:
        dict: A dictionary containing the metadata of the Zarr array.
    """
    return {
        "path": zarray.path,
        "type": "zarray",
        "shape": list(zarray.shape),
        "dtype": str(zarray.dtype),
        "chunks": list(zarray.chunks),
        "order": zarray.order,
        "read_only": zarray.read_only,
        "compressor": str(zarray.compressor) if zarray.compressor else None,
        "filters": [str(f) for f in zarray.filters] if zarray.filters else [],
        "fill_value": __convert_to_json_serializable_recursive(zarray.fill_value),
        "ndim": zarray.ndim,
        "itemsize": zarray.itemsize,
        "nbytes": int(zarray.nbytes),
        "nchunks": int(zarray.nchunks),
        "cdata_shape": list(zarray.cdata_shape),
        "attrs": __convert_to_json_serializable_recursive(dict(zarray.attrs)),
    }

def __convert_to_json_serializable_recursive(value: object) -> object:
    """Converts an object to a JSON-serializable format, 
    handling various types including NumPy arrays, scalars, and datetime objects.

    Args:
        value (object): The object to convert.

    Returns:
        object: A JSON-serializable representation of the input object.
    """
    if isinstance(value, dict):
        return {k: __convert_to_json_serializable_recursive(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return [__convert_to_json_serializable_recursive(elem) for elem in value]
    # Convert NumPy scalar to Python scalar
    elif isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item()
    # Handle NumPy arrays by summarizing shape and dtype
    elif isinstance(value, np.ndarray):
        return f"ndarray(shape={value.shape}, dtype={value.dtype})"
    # For datetime-like objects (e.g., pandas Timestamps, numpy datetime64)
    elif hasattr(value, 'isoformat'): 
        try:
            return value.isoformat()
        except AttributeError:
            return str(value)
    # Decode bytes to string
    elif isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    # Already JSON serializable types
    elif value is None or isinstance(value, (int, float, bool, str)):
        return value 
    else:
        # Fallback for any other custom object type not explicitly handled
        try:
            return str(value)
        except Exception:
            return f"<Unserializable object of type {type(value)}>"

def _find_all_attribute_names_recursive(metadata_dict, current_path="") -> set:
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
                    _find_all_attribute_names_recursive(value, full_path_key)
                )
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    attribute_names.update(
                        _find_all_attribute_names_recursive(item, f"{full_path_key}[{i}]")
                    )
            else:
                attribute_names.add(full_path_key)

    return attribute_names