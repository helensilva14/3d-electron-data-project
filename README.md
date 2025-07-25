# 3D Electron Microscopy - Data Acquisition and Preparation

This project automates the acquisition, metadata extraction, and consolidation of publicly available 3D electron microscopy datasets, with the future goal of enabling efficient, block-wise access for AI/ML pipelines.

## Project Goals

1. **Automated Data Download:** Robust scripts to download diverse 3D electron microscopy datasets from multiple sources.
1. **Metadata Extraction & Consolidation:** Identify, extract, and harmonize relevant metadata (e.g., attrs, chunks) from each dataset, providing a unified and queryable view (see [`METADATA_SUMMARY.md`](docs/METADATA_SUMMARY.md)).
1. **AI/ML Pipeline Data Access Design:** Outline and prototype a strategy for block-wise access to large 3D image datasets for scalable AI/ML workflows (see [`DATA_ACCESS_DESIGN.md`](docs/DATA_ACCESS_DESIGN.md)).

## Datasets

The following publicly available 3D electron microscopy datasets are targeted:

1. **EMPIAR-11759:** [https://www.ebi.ac.uk/empiar/EMPIAR-11759/](https://www.ebi.ac.uk/empiar/EMPIAR-11759/)
1. **EPFL-Hippocampus:** [https://www.epfl.ch/labs/cvlab/data/data-em/](https://www.epfl.ch/labs/cvlab/data/data-em/)
1. **Hemibrain-NG:** [https://tinyurl.com/hemibrain-ng](https://tinyurl.com/hemibrain-ng) (Note: Only a random 1000x1000x1000 pixel crop region will be downloaded for this dataset.)
1. **JRC-MUS-NACC:** [https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2](https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2)
1. **U2OS-Chromatin:** [https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740](https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740)

## Tools & Dependencies

- **Python 3.12**
- **[DVC](https://dvc.org/)** (optional, for data versioning)
- **tifffile** for handling TIFF files
- **cloud-volume** for Neuroglancer data
- **zarr** for scalable array storage
- **pyDM3reader** for DM3 files
- **requests**, **ftplib** for downloads
- **pandas** for summary tables
- See [`requirements.txt`](requirements.txt) for the full list

## Installation & Usage

```bash
git clone https://github.com/helensilva14/3d-electron-data-project.git
cd 3d-electron-data-project

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run the main pipeline (downloads data, extracts metadata, consolidates):

```bash
python3 src/main.py
```

Outputs will be saved in the `outputs/` and `docs/` directories.

## License

This project is licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).