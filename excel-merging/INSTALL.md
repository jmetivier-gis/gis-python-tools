# 🔧 Installation in ArcGIS Pro

1 - Open ArcGIS Pro.

2 - In the Catalog pane, right-click an existing Toolbox (or create a new one):

- Right click → Add → Toolbox

3 - Right-click the Toolbox → Add → Script.

4 - Script Properties

- Name: ExcelMerge

- Label: Excel Merge (CSV + SHP)

- Script File: select excel-merging-tools/tools/fusion_xlsx.py

5 - Parameters (add in this order):

| # | Label      | Name            | Data Type | Required |
| - | ---------- | --------------- | --------- | -------- |
| 1 | Date tag   | date_fichier    | String    | Yes      |


Notes
- The script reads all .xlsx from a fixed input folder, merges rows (sheet "AAAA"), then writes a timestamped CSV and Shapefile (WGS84/EPSG:4326).
- If you want to avoid fixed paths, make input/output folders and X/Y fields parameters in a future version.

6 - Click OK to save. The tool appears in your Toolbox.

7 - Run the tool and set e.g. 2025-09-30 for Date tag.

- Outputs are written to the fixed output folders defined in the script.

---------------------------------
⚠️ Troubleshooting

If no files found: check the input folder path inside the script.

If columns missing: ensure Longitude décimale / Latitude décimale exist in the Excel files.

If projection issues: outputs are in WGS84 (EPSG:4326).
