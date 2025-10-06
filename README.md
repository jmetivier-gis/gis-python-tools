# GIS Python Tools 🗺️🐍

## 📌 Overview
This repository is a collection of **Python tools for GIS automation** using  
[ArcPy](https://pro.arcgis.com/en/pro-app/arcpy/) and [pandas](https://pandas.pydata.org/).  
The goal is to provide reusable scripts and ArcGIS Pro script tools for data preprocessing, analysis, and reporting.  

It is organized into **modules** (by theme), each containing scripts, examples, and documentation.  

It includes three functional modules:
- **OSM Sorting & Export** — process and filter OpenStreetMap data by `fclass`, apply buffers and exclusion zones  
- **Change Detection** — compare old and new GIS datasets, compute geodesic areas and generate change reports  
- **Excel Merging** — merge multiple Excel files, export results to CSV and Shapefile  

Each module can be used independently as a **Script Tool in ArcGIS Pro** or through the global Python Toolbox.

⚠️ Note: scripts currently use **French variable names and log messages**.  
All documentation, READMEs and usage instructions are provided in **English** for clarity.

---

## Repository Structure
```
gis-python-tools/
├─ README.md
├─ LICENSE
├─ requirements.txt
│
├─ toolbox/
│ └─ global_tools.pyt ← single ArcGIS Pro toolbox (3 tools)
│
├─ osm-sorting-export/
│ ├─ README.md
│ ├─ INSTALL.md
│ ├─ tools/
│ │ └─ osm_sort_export.py
│
├─ change-detection-tools/
│ ├─ README.md
│ ├─ INSTALL.md
│ ├─ tools/
│ │ └─ change_detection.py
│
└─ excel-merging-tools/
  ├─ README.md
  ├─ INSTALL.md
  ├─ tools/
  │ └─ fusion_xlsx.py
```


## 🔧 Modules

| Module | Description | Main script |
|---------|--------------|--------------|
| [OSM Sorting & Export](osm-sorting-export/) | Split OSM shapefiles by `fclass`, apply buffers, and exclude zones | [osm_sort_export.py](osm-sorting-export/tools/osm_sort_export.py) |
| [Change Detection](change-detection/) | Compare two datasets (old/new), compute area deltas and generate reports | [change_detection.py](change-detection/tools/change_detection.py) |
| [Excel Merging](excel-merging/) | Merge multiple `.xlsx` files, create CSV and Shapefile outputs | [fusion_xlsx.py](excel-merging/tools/fusion_xlsx.py) |

---

## 🧰 ArcGIS Pro Toolbox
A single **Python toolbox** ([`global_tools.pyt`](global-py-toolbox/global_tools.pyt)) groups all three tools under one ArcGIS Pro interface:

| Tool name | Description |
|------------|--------------|
| **OSM Sorting & Export** | Extracts and exports OSM layers by category and road type |
| **Excel Merge (CSV + SHP)** | Merges Excel files and creates shapefile outputs |
| **Change Detection (Counts & Areas)** | Compares datasets and reports changes by type and country |

Each module also includes its own **`INSTALL.md`** for standalone setup in ArcGIS Pro.

---

## ⚙️ Requirements
- **ArcGIS Pro** (tested with 3.x)
- **Python 3.9+** (ArcGIS Pro environment)
- Python packages:
  - pandas>=2.0.0
  - openpyxl>=3.1.0
  - arcpy (bundled with ArcGIS Pro)

 Install Python packages (outside ArcGIS Pro):
```bash
pip install -r requirements.txt
```


## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with attribution.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Made%20with-Python-green.svg)


## 👤 Author

Jordan Metivier
GIS Analyst | Python & ArcGIS Automation
🔗 [LinkedIn](https://www.linkedin.com/in/jordan-m-52b404a5/)
 | [GitHub](https://github.com/jmetivier-gis/)
