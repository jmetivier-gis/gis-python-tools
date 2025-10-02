# 🔧 Installation in ArcGIS Pro (EN)

1 - Open ArcGIS Pro.

2 - In the Catalog pane, right-click an existing Toolbox (or create a new one):

- Right click → Add → Toolbox

3 - Right-click the Toolbox → Add → Script.

4 - Script Properties

- Name: OSMSortExport

- Label: OSM Sorting & Export (fclass + buffers)

- Script File: select osm-sorting-export/tools/osm_sort_export.py.

5 - Parameters (add in this exact order):

| # | Label             | Name            | Data Type                     | Required |
| - | ----------------- | --------------- | ----------------------------- | -------- |
| 1 | Input folder      | input_folder    | **Folder**                    | Yes      |
| 2 | Output folder     | output_folder   | **Folder**                    | Yes      |
| 3 | Zone A layer      | zone_a_layer    | **Feature Class / Layer**     | Yes      |
| 4 | Zone B layer      | zone_b_layer    | **Feature Class / Layer**     | Yes      |
| 5 | Buffer A distance | buffer_a_dist   | **Linear Unit** *(or String)* | Yes      |
| 6 | Buffer B distance | buffer_b_dist   | **Linear Unit** *(or String)* | Yes      |
| 7 | Exclusion layer   | exclusion_layer | **Feature Class / Layer**     | No       |


Notes
- Linear Unit gives a nicer UX (e.g. 200 Meters); the script reads it as text.
- Zone A applies to all categories except tertiary roads; Zone B applies to tertiary roads only.
- Exclusion layer (optional) is removed from selections before export.

6 - Click OK to save. The tool appears in your Toolbox.

7 - Run the tool by setting the folders, zones, buffer distances, and (optionally) an exclusion layer.

✅ Expected outputs

- For each relevant OSM layer (e.g., Landuse/Natural/Places/Water…): individual shapefiles exported per fclass, filtered by buffer(s) and minus the exclusion zone.

- For roads: three shapefiles (e.g., Routes principales, Routes secondaires, Routes tertiaires) built using the correct buffer (A or B) and the exclusion rule.
