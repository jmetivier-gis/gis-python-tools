# 🔧 Installation in ArcGIS Pro

1 - Open ArcGIS Pro.

2 - In the Catalog pane, right-click a Toolbox (or create a new one):

- Right click → Add → Toolbox

3 - Right-click the Toolbox → Add → Script.

4 - Script Properties:

- Name: ChangeDetection

- Label: Change Detection – Counts & Areas

- Script File: select the Python file in this module, e.g. tools/change_detection.py

5 - Open the Parameters tab and add the inputs in this exact order:


| # | Label         | Name            | Data Type         | Required |
| - | ------------- | --------------- | ----------------- | -------- |
| 1 | Old layer     | old_layer       | **Feature Class** | Yes      |
| 2 | New layer     | new_layer       | **Feature Class** | Yes      |
| 3 | Country field | country_field   | **String**        | No       |
| 4 | Type field    | type_field      | **String**        | Yes      |
| 5 | Output folder | out_folder      | **Folder**        | Yes      |


6 - Click OK to save. The tool now appears in your Toolbox.

7 - Run the tool: pick the two layers, set the fields, choose an output folder.

- The geodesic-area comparison report path is printed in the geoprocessing messages.


-------------------------------

⚠️ Notes & Troubleshooting

Polygons expected for area comparisons. Repair invalid geometries before running.

Field names must exist in both datasets (Type is required; Country is optional).

Areas are computed geodesically (km²), independent of the layer projection.

If you see “field not found” or empty groups, verify attribute names and null values.
