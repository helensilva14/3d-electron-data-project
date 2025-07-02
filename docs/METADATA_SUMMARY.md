# Metadata Summary & Strategy


<table>
  <tr>
    <th>Script</th>
    <th>File Type</th>
  </tr>
  <tr>
    <td>empiar_11759.py</td>
    <td rowspan="1">DM3 format</td>
  </tr>
  <tr>
    <td>hemibrain_ng.py</td>
    <td rowspan="2">ZARR format</td>
  </tr>
  <tr>
    <td>jrc_mus_nacc.py</td>
  </tr>
  <tr>
    <td>epfl_hippocampus.py</td>
    <td rowspan="2">TIFF format</td>
  </tr>
  <tr>
    <td>u2os_chromatin.py</td>

TODO:
- Write consolidation functions for each group: DM3, ZARR, TIFF
- Based on the extension, point each JSON to its corresponding consolidation function
- Perform a final consolidation on top of the groups (same or equivalent attributes)
