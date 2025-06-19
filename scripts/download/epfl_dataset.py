from utils.helpers import download_tif_file

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
OUTPUT_PATH = "volumedata.tif"

def download():
    """
    Downloads the EPFL Electron Microscopy Hippocampus dataset.
    """
    print("Started download of EPFL Electron Microscopy Hippocampus dataset...")
    download_tif_file(DATASET_URL, OUTPUT_PATH)
    print("Finished download of EPFL Electron Microscopy Hippocampus dataset.")