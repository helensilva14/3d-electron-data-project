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
ALL_METADATA_FILE = "outputs/jrc_mus_nacc_2_all_metadata.json"

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

def _process_xarray_dict_attributes(xarray_dict_like_obj):
    """
    Processes a dictionary-like object (like .coords or .attrs) from Xarray.
    If a value is an Xarray object, it summarizes it to prevent deep recursion.
    """
    if not hasattr(xarray_dict_like_obj, 'items'): # Ensure it's dict-like
        return {}

    processed_dict = {}
    for k, v in xarray_dict_like_obj.items():
        if isinstance(v, (xr.DataArray, xr.DataTree)):
            # Summarize Xarray objects within coords/attrs to break recursion cycles
            processed_dict[k] = {
                "type": "DataArray (summarized)" if isinstance(v, xr.DataArray) else "DataTree (summarized)",
                "shape": v.shape if hasattr(v, 'shape') else None,
                "dtype": str(v.dtype) if hasattr(v, 'dtype') else None,
                "dims": list(v.dims) if hasattr(v, 'dims') else [],
                # Do NOT recurse into v.coords or v.attrs here
                "summary_only": True
            }
        else:
            # For other types, use the general serialization function
            processed_dict[k] = _to_json_serializable(v)
    return processed_dict

def _to_json_serializable(obj):
    # Handle basic JSON-serializable types first to avoid unnecessary recursion or complex checks
    if obj is None or isinstance(obj, (int, float, bool, str)):
        return obj
    elif isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item() # Convert NumPy scalars to Python native types
    elif hasattr(obj, 'isoformat'): # For datetime objects (e.g., pandas Timestamps)
        return obj.isoformat()
    
    elif isinstance(obj, xr.DataTree):
        # Extract direct properties
        result = {
            "type": "DataTree",
            # DataTree.dims is usually a tuple of its children's dims, convert to list
            "dims": list(obj.dims) if hasattr(obj, 'dims') and obj.dims is not None else [],
        }
        # Handle its own attributes and coordinates similarly
        result["coords"] = _process_xarray_dict_attributes(obj.coords) if hasattr(obj, 'coords') else {}
        result["attrs"] = _process_xarray_dict_attributes(obj.attrs) if hasattr(obj, 'attrs') else {}
        return result

    # Handle standard Python collections (dictionaries and lists/tuples)
    # This comes AFTER Xarray objects to ensure they are caught by their specific handlers
    elif isinstance(obj, dict):
        return {k: _to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_to_json_serializable(elem) for elem in obj]

    # Fallback for any other iterable/mapping (e.g., xarray's internal Frozen objects)
    # This needs to be at the end to catch anything not explicitly handled.
    elif hasattr(obj, '__iter__') and not isinstance(obj, str):
        try:
            # Try to convert to dict
            return _to_json_serializable(dict(obj))
        except TypeError:
            # If dict() fails, try converting to list
            return _to_json_serializable(list(obj))
    else:
        return str(obj) # Force conversion to string if truly unhandled

def extract_metadata():
    """Extracts metadata from the downloaded Zarr container and saves it to a JSON file."""
    dtree = fibsem_tools.read_xarray(SAVE_PATH)
    extracted_metadata = {}

    # 1. Get top-level DataTree attributes
    if dtree.attrs:
        # Pass DataTree attrs to the new helper
        extracted_metadata['root_attrs'] = _process_xarray_dict_attributes(dtree.attrs)

    # 2. Traverse children (DataArrays and nested DataTrees)
    child_metadata = {}
    for name, node in dtree.items():
        child_metadata[name] = _to_json_serializable(node) # This will correctly handle DataArray/DataTree children

    extracted_metadata['children_metadata'] = child_metadata

    save_metadata_as_json(extracted_metadata, METADATA_FILE)

def run_tasks():
    """Runs the download and metadata extraction tasks."""
    download_dataset()
    extract_metadata()