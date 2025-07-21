# Metadata Summary & Consolidation

1. **[EMPIAR-11759](/outputs/empiar_11759_metadata):** 16 metadata files with 400+ original tags each, besides the 21 top-level and fixed attributes.
1. **[EPFL-Hippocampus:](/outputs/epfl_hippocampus_tif_metadata.json)** single file with information about all the 1065 pages.
1. **[Hemibrain-NG:](/outputs/hemibrain_ng_zarr_metadata.json)** single file with only 1 zarray and its attributes.
1. **[JRC-MUS-NACC:](/outputs/jrc_mus_nacc_zarr_metadata.json)** single file with attributes about 1 zgroup and attributes for each one of its 8 zarrays.
1. **[U2OS-Chromatin:](/outputs/u2os_chromatin_metadata)** 2 metadata files (one for XY, other XZ) with each file having information about all the 184 pages.

My strategy for the overall consolidation between all datasets consisted in identifying and organizing all top-level metadata categories from the JSON metadata files. 
- A key function [`__get_top_level_metadata_categories`](/src/utils/metadata.py#L319) extracted these categories, looking in standard locations and also deeper within format-specific sections of each dataset file type (DM3, ZARR, TIFF)
- Then, the main consolidation function [`consolidate_categories`](/src/utils/metadata.py#L183) tracked which categories appeared in multiple metadata files and which were unique to single files. This resulted in a clear summary of all categories and their distribution across the datasets. This final consolidation result is available in the [consolidated_metadata.json](consolidated_metadata.json) file.

Below there is a table with a manual and high-level summary of the metadata values present in the datasets. Last but not least there is a table with the `categories_in_multiple_datasets` section of the result file, sorted alphabetically by category name.

## Table - Metadata Values Summary

<table border="1"><thead>
  <tr>
    <th>Dataset</th>
    <th>Size</th>
    <th>Resolution</th>
    <th>DataType</th>
    <th>Chunks</th>
    <th>Compressor</th>
  </tr></thead>
<tbody>
  <tr>
    <td>EMPIAR-11759</td>
    <td>5496x5500x1</td>
    <td>0.0080x0.0080x0.0080 µm</td>
    <td>UNSIGNED_INT8_DATA</td>
    <td><i>N/A</i></td>
    <td><i>N/A</i></td>
  </tr>
  <tr>
    <td>EPFL-Hippocampus</td>
    <td>1065x2048x1536</td>
    <td>5x5x5 nm</td>
    <td>uint8</td>
    <td><i>N/A</i></td>
    <td><i>N/A</i></td>
  </tr>
  <tr>
    <td>Hemibrain-NG</td>
    <td>1000x1000x1000</td>
    <td>8x8x8 nm</td>
    <td>uint64</td>
    <td>[63, 63, 125, 1]</td>
    <td>Blosc(cname='lz4', clevel=5, shuffle=SHUFFLE, blocksize=0)</td>
  </tr>
  <tr>
    <td>JRC-MUS-NACC</td>
    <td>10384x10080x1669.44 nm</td>
    <td>4x4x2.96 nm</td>
    <td>int16</td>
    <td>[64, 64, 64]</td>
    <td>Zstd(level=1)</td>
  </tr>
  <tr>
    <td>U2OS-Chromatin</td>
    <td>xy = 1121x775x1, <br>xz = 1121x184x1</td>
    <td>0.02x0.02x0.02 µm</td>
    <td>uint8</td>
    <td><i>N/A</i></td>
    <td><i>N/A</i></td>
  </tr>
</tbody>
</table>

## Table - Metadata Fields Summary 

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Category name</th>
      <th>Present in the following files</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>acq_date</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>acq_time</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
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
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>dtype</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata, hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>file_version</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>filename</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
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
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>global_info</td>
      <td>[Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy_tif_metadata, Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz_tif_metadata, epfl_hippocampus_tif_metadata]</td>
    </tr>
    <tr>
      <td>gms_v</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>gms_v_</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>hv</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>hv_f</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>image_summary</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>info</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>itemsize</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
    <tr>
      <td>mag</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>mag_f</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>micro</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>mode</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>name_old</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
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
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
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
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>pixel_size_value</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
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
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>specimen</td>
      <td>[F57-8_test1_3VBSED_slice_00**_dm3_metadata]</td>
    </tr>
    <tr>
      <td>type</td>
      <td>[hemibrain_ng_zarr_metadata, jrc_mus_nacc_zarr_metadata]</td>
    </tr>
  </tbody>
</table>