# 3D Electron Microscopy Dataset Acquisition and Preparation

This project aims to acquire publicly available 3D electron microscopy datasets, extract and consolidate their metadata, and design a strategy for making them accessible to AI/ML pipelines in a block-wise manner.

-----

## Project Goal

The primary goals of this project are:

1.  **Automated Data Download:** Develop robust and efficient code to download diverse 3D electron microscopy datasets from various sources.
2.  **Metadata Consolidation:** Identify, extract, and consolidate relevant metadata (e.g., resolution, pixel type) from these datasets, providing a unified view.
3.  **AI/ML Pipeline Data Access Design:** Outline a software design for providing block-wise access to these large 3D image datasets for AI/ML model training and inference.

-----

## Datasets

The following publicly available 3D electron microscopy datasets are targeted for this project:

  * **IDR:** [https://idr.openmicroscopy.org/webclient/img\_detail/9846137/?dataset=10740](https://idr.openmicroscopy.org/webclient/img_detail/9846137/?dataset=10740)
  * **EMPIAR:** [https://www.ebi.ac.uk/empiar/EMPIAR-11759/](https://www.ebi.ac.uk/empiar/EMPIAR-11759/)
  * **EPFL CVLAB:** [https://www.epfl.ch/labs/cvlab/data/data-em/](https://www.epfl.ch/labs/cvlab/data/data-em/)
  * **Janelia OpenOrganelle:** [https://openorganelle.janelia.org/datasets/jrc\_mus-nacc-2](https://openorganelle.janelia.org/datasets/jrc_mus-nacc-2)
  * **Hemibrain-NG:** [https://tinyurl.com/hemibrain-ng](https://tinyurl.com/hemibrain-ng) (Note: Only a random 1000x1000x1000 pixel crop region will be downloaded for this dataset.)

-----

## Tasks

### 1\. Data Download

Develop a set of scripts or a small application to download the specified datasets. Given the varied storage mechanisms, the download process should ideally leverage parallel and multi-threaded approaches for efficiency. The code should be reproducible, allowing others to easily download the same datasets.

**Deliverables:**

  * Python scripts (or similar) for downloading each dataset.
  * Instructions on how to run the download scripts.
  * Error handling for robust downloads.

### 2\. Metadata Identification and Consolidation

Identify common and unique metadata entries across the downloaded datasets. This includes, but is not limited to, `resolution` and `pixel type`. Extract all available metadata and consolidate it into a structured format (e.g., a CSV or JSON file). A summary of the extraction methodology will also be provided.

**Deliverables:**

  * Scripts for metadata extraction.
  * Consolidated metadata table (e.g., `metadata.csv` or `metadata.json`).
  * `METADATA_SUMMARY.md` explaining the extraction process and findings.

### 3\. AI/ML Pipeline Data Access Design

Design a conceptual software architecture for making these large 3D image datasets available for AI/ML pipelines in a block-wise manner. The design should consider how an ML software would request specific 128x128x128 pixel blocks at various locations within each dataset. This task focuses on the design and outline, not on a full implementation.

**Deliverables:**

  * `DATA_ACCESS_DESIGN.md` outlining the proposed architecture, considerations, and potential technologies.

-----

## Getting Started

### Prerequisites

  * **Python 3.x**
  * (Potentially) Specific libraries for handling different image formats (e.g., `zarr`, `h5py`, `tifffile`, `ome-zarr`, `python-omero`)

### Installation

No specific installation steps beyond cloning the repository and ensuring Python dependencies are met.

```bash
git clone https://github.com/helensilva14/3d-electron-data-project.git
cd 3d-electron-data-project
pip install -r requirements.txt
```

### Usage

Detailed instructions for running download scripts, metadata extraction, and accessing design documents will be provided in their respective subdirectories.

-----

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

---

## License

This project is licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
