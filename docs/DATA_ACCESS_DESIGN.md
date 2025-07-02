# Data Access Design for AI/ML Pipelines

## High-Level Goals

- **Abstraction:** Hide format and storage details behind a common interface.
- **Efficiency:** Load only the required data blocks, minimizing I/O and memory usage.
- **Extensibility:** Easily add new formats or storage backends.
- **Metadata Sharing:** Expose relevant metadata (shape, dtype, resolution, etc.) alongside data.

## Proposed Architecture - Unified Data Access API

Create a high-level Python interface (`VolumeDataset`) with methods such as:
- `get_block(start_xyz, block_size=(128,128,128))`: Returns a numpy array or Tensor for the specified block.
- `get_metadata()`: Returns a metadata dictionary for the dataset.

Implement format-specific backends:
- `TiffVolumeDataset`
- `ZarrVolumeDataset`
- `DM3VolumeDataset`
