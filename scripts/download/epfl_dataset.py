from utils.helpers import download_file

DATASET_URL = "https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif"
OUTPUT_PATH = "volumedata.tif"

def download_epfl():
    """
    Downloads the EPFL Electron Microscopy Hippocampus dataset.
    """
    print("Started download of EPFL Electron Microscopy Hippocampus dataset...")

    download_file(DATASET_URL, OUTPUT_PATH)
    # TODO: print elapsed time for download

    print("Finished download of EPFL Electron Microscopy Hippocampus dataset.")