import os
import quilt3 as q3
import fibsem_tools
import numpy as np
import xarray as xr

from timeit import default_timer as timer
from utils.helpers import save_metadata_as_json

BUCKET_ROOT = "s3://janelia-cosem-datasets"
INTERNAL_PATH = "jrc_mus-nacc-2/jrc_mus-nacc-2.zarr/recon-2/em/fibsem-int16/"

SAVE_PATH = "data/raw/jrc_mus_nacc_2.zarr/"
METADATA_FILE = "outputs/jrc_mus_nacc_2_metadata.json"

def download_dataset():
    """Downloads the Janelia Mouse nucleus accumbens dataset."""
    try:
        if os.path.exists(SAVE_PATH):
            print(f"\nDataset already exists at {SAVE_PATH}. Skipping download.")
        else:
            print(f"\nDataset not found at {SAVE_PATH}. Proceeding with download...")
            start_time = timer()

            bucket = q3.Bucket(BUCKET_ROOT)
            bucket.fetch(INTERNAL_PATH, SAVE_PATH)

            end_time = timer()
            print(f"Download completed in {(end_time - start_time):.2f} seconds.")
    except Exception as e:
        print(f"\nError downloading {BUCKET_ROOT}/{INTERNAL_PATH}: {e}")

def _process_xarray_dict_items(xarray_dict_like_obj) -> dict:
    """
    Processes a dictionary-like object (like .coords or .attrs) from Xarray.
    If a value is an Xarray object, it summarizes it to prevent deep recursion in the serialization function.

    Args:
        xarray_dict_like_obj (dict-like): The Xarray dictionary-like object to process.

    Returns:
        dict: A JSON-serializable dictionary with summarized Xarray objects.
    """
    # Ensure it's dict-like
    if not hasattr(xarray_dict_like_obj, 'items'):
        return {}

    processed_dict = {}
    for key, value in xarray_dict_like_obj.items():
        if isinstance(value, (xr.DataArray, xr.DataTree)):
            # Summarize Xarray objects within coords/attrs to break recursion cycles
            processed_dict[key] = {
                "type": "DataArray (summarized)" if isinstance(value, xr.DataArray) else "DataTree (summarized)",
                "shape": value.shape if hasattr(value, 'shape') else None,
                "dtype": str(value.dtype) if hasattr(value, 'dtype') else None,
                "dims": list(value.dims) if hasattr(value, 'dims') else [],
                # IMPORTANT: not recursing into value.coords or value.attrs here
                "summary_only": True
            }
        else:
            processed_dict[key] = _to_json_serializable_recursive(value)
    
    return processed_dict

def _to_json_serializable_recursive(obj) -> object:
    """ Recursively converts an object to a JSON-serializable format.
    Handles various data types, including NumPy arrays, Xarray DataArrays, and other complex objects.
    
    Args:
        obj: The object to convert to a JSON-serializable format.
    
    Returns:
        A JSON-serializable version of the object.
    """
    # Basic JSON-serializable types first to avoid unnecessary recursion or complex checks
    if obj is None or isinstance(obj, (int, float, bool, str)):
        return obj
    # Convert NumPy scalars to Python native types
    elif isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    # For datetime objects (e.g., pandas Timestamps)
    elif hasattr(obj, 'isoformat'): 
        return obj.isoformat()
    
    elif isinstance(obj, xr.DataTree):
        obj_as_dict = {
            "type": "DataTree",
            "dims": list(obj.dims) if hasattr(obj, 'dims') and obj.dims is not None else [],
        }
        obj_as_dict["coords"] = _process_xarray_dict_items(obj.coords) if hasattr(obj, 'coords') else {}
        obj_as_dict["attrs"] = _process_xarray_dict_items(obj.attrs) if hasattr(obj, 'attrs') else {}
        return obj_as_dict

    # Python collections AFTER Xarray objects to ensure they are caught by their specific handlers
    elif isinstance(obj, dict):
        return {k: _to_json_serializable_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_to_json_serializable_recursive(elem) for elem in obj]

    # Fallback for any other iterable/mapping (e.g., xarray's internal Frozen objects)
    # This needs to be at the end to catch anything not explicitly handled.
    elif hasattr(obj, '__iter__') and not isinstance(obj, str):
        try:
            return _to_json_serializable_recursive(dict(obj))
        except TypeError:
            # If dict() conversion fails, default to list conversion
            return _to_json_serializable_recursive(list(obj))
    else:
        # Force conversion to string if truly unhandled after all checks
        return str(obj) 

def extract_metadata():
    """Extracts metadata from the downloaded Zarr container and saves it to a JSON file."""
    try:
        if os.path.exists(METADATA_FILE):
            print(f"Metadata file already exists at {METADATA_FILE}. Skipping extraction.")
        else:
            print(f"Metadata file not found at {METADATA_FILE}. Proceeding with extraction...")
            start_time = timer()
            extracted_metadata = {}
            
            # Load previously downloaded Zarr container
            datatree = fibsem_tools.read_xarray(SAVE_PATH)

            # Get top-level DataTree attributes
            if datatree.attrs:
                extracted_metadata['root_attrs'] = _process_xarray_dict_items(datatree.attrs)

            # Get info from all DataTree items (DataArrays and nested DataTrees)
            child_metadata = {}
            for name, node in datatree.items():
                child_metadata[name] = _to_json_serializable_recursive(node)
            
            extracted_metadata['children_metadata'] = child_metadata
            # Save metadata to a JSON file
            save_metadata_as_json(extracted_metadata, METADATA_FILE)

            end_time = timer()
            print(f"Metadata extraction completed in {(end_time - start_time):.2f} seconds.")

    except Exception as e:
        print(f"\nError extracting metadata from {SAVE_PATH}: {e}")

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()