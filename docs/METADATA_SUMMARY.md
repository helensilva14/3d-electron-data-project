# Metadata Consolidation

My strategy consisted in identifying and organizing all top-level metadata categories from the JSON metadata files. 
- A key function [`__get_top_level_metadata_categories`](/src/utils/metadata.py#L319) extracted these categories, looking in standard locations and also deeper within format-specific sections of each dataset file type (DM3, ZARR, TIFF)
- Then, the main consolidation function [`consolidate_categories`](/src/utils/metadata.py#L183) tracked which categories appeared in multiple metadata files and which were unique to single files. This resulted in a clear summary of all categories and their distribution across the datasets. This final consolidation result is available in the [consolidated_metadata.json](consolidated_metadata.json) file.

Below there is a table with the `categories_in_multiple_datasets` section of the result file, sorted alphabetically by category name.

## Ideal next steps:
- Analyze list of filenames to detect sequential patterns and summarize them.
  - Current problem: all DM3 files being listed on consolidated_metadata.json when only the common prefix could be used
- Generate other tables to compare the values of the common categories between the datasets.

## Table - Metadata Summary 

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>category_name</th>
      <th>present_in_files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>acq_date</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>acq_time</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>attrs</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>cdata_shape</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>chunks</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>compressor</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>cuts</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>dtype</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata, hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>file_version</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>filename</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>fill_value</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>filters</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>full_original_tags</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>global_info</td>
      <td>[Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy_tif_metadata, Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz_tif_metadata, epfl_hippocampus_tif_metadata]</td>
    </tr>
    <tr>
      <td>gms_v</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>gms_v_</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>hv</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>hv_f</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>image_summary</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>info</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>itemsize</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>mag</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>mag_f</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>micro</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>mode</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>name_old</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>nbytes</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>nchunks</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>ndim</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>operator</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>order</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>pages</td>
      <td>[Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy_tif_metadata, Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz_tif_metadata, epfl_hippocampus_tif_metadata]</td>
    </tr>
    <tr>
      <td>path</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>pixel_size_unit</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>pixel_size_value</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>read_only</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>shape</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>size</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>specimen</td>
      <td>[F57-8_test1_3VBSED_slice_0000_dm3_metadata, F57-8_test1_3VBSED_slice_0001_dm3_metadata, F57-8_test1_3VBSED_slice_0002_dm3_metadata, F57-8_test1_3VBSED_slice_0003_dm3_metadata, F57-8_test1_3VBSED_slice_0004_dm3_metadata, F57-8_test1_3VBSED_slice_0005_dm3_metadata, F57-8_test1_3VBSED_slice_0006_dm3_metadata, F57-8_test1_3VBSED_slice_0007_dm3_metadata, F57-8_test1_3VBSED_slice_0008_dm3_metadata, F57-8_test1_3VBSED_slice_0009_dm3_metadata, F57-8_test1_3VBSED_slice_0010_dm3_metadata, F57-8_test1_3VBSED_slice_0011_dm3_metadata, F57-8_test1_3VBSED_slice_0012_dm3_metadata, F57-8_test1_3VBSED_slice_0013_dm3_metadata, F57-8_test1_3VBSED_slice_0014_dm3_metadata, F57-8_test1_3VBSED_slice_0015_dm3_metadata]</td>
    </tr>
    <tr>
      <td>type</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
  </tbody>
</table>