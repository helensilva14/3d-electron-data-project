# 3D Electron Microscopy Dataset Acquisition and Preparation

This project aims to acquire publicly available 3D electron microscopy datasets, extract and consolidate their metadata, and design a strategy for making them accessible to AI/ML pipelines in a block-wise manner.

## Project Goal

The primary goals of this project are:

1.  **Automated Data Download:** Develop robust and efficient code to download diverse 3D electron microscopy datasets from various sources.
2.  **Metadata Consolidation:** Identify, extract, and consolidate relevant metadata (e.g., resolution, pixel type) from these datasets, providing a unified view.
3.  **AI/ML Pipeline Data Access Design:** Outline a software design for providing block-wise access to these large 3D image datasets for AI/ML model training and inference.

## Datasets

The following publicly available 3D electron microscopy datasets are targeted for this project:

  * **IDR:** [https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740](https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740)
  * **EMPIAR:** [https://www.ebi.ac.uk/empiar/EMPIAR-11759/](https://www.ebi.ac.uk/empiar/EMPIAR-11759/)
  * **EPFL CVLAB:** [https://www.epfl.ch/labs/cvlab/data/data-em/](https://www.epfl.ch/labs/cvlab/data/data-em/)
  * **Janelia OpenOrganelle:** [https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2](https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2)
  * **Hemibrain-NG:** [https://tinyurl.com/hemibrain-ng](https://tinyurl.com/hemibrain-ng) (Note: Only a random 1000x1000x1000 pixel crop region will be downloaded for this dataset.)

## Tasks

### 1. Data Download

Scripts are provided for downloading each dataset. The download process leverages chunked streaming for large files and is designed to be reproducible.

**Current Status:**
- [x] EPFL dataset download implemented ([`epfl_dataset.py`](src/download/epfl_dataset.py))
- [ ] U2OS Chromatin download script stub ([`u2os_chromatin_dataset.py`](src/download/u2os_chromatin_dataset.py))
- [ ] EMPIAR, Janelia, and Hemibrain download scripts are stubbed and need implementation

### 2. Metadata Identification and Consolidation

Scripts extract both brief and full metadata from TIFF files using Pillow and tifffile. Metadata is saved as JSON.

**Current Status:**
- [x] Metadata extraction for TIFF files ([`metadata.py`](src/utils/metadata.py))
- [x] Metadata extraction for EPFL dataset ([`epfl_dataset.py`](src/download/epfl_dataset.py))
- [ ] Metadata extraction for other formats (e.g., Zarr) is planned

**Deliverables:**
- [x] Scripts for metadata extraction ([`src/utils/metadata.py`](src/utils/metadata.py))
- [ ] Consolidated metadata table (planned)
- [ ] `METADATA_SUMMARY.md` (in progress)

### 3. AI/ML Pipeline Data Access Design

A conceptual design for block-wise access is outlined in [`DATA_ACCESS_DESIGN.md`](docs/DATA_ACCESS_DESIGN.md).

## Tools & Dependencies

- **Python 3.12**
- **DVC** for data versioning (usage is optional)
- **Pillow** and **tifffile** for TIFF handling
- **requests** for HTTP downloads
- **zarr**, **h5py**, **xarray** for scalable array data (planned)
- See [`requirements.txt`](requirements.txt) for the full list

## Installation & Execution

```bash
git clone https://github.com/helensilva14/3d-electron-data-project.git
cd 3d-electron-data-project
pip install -r requirements.txt
```

Run the main script to execute the project tasks:
```bash
python3 src/main.py
```

-----

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
