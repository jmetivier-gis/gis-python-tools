# GIS Python Tools 🗺️🐍

## 📌 Overview
This repository is a collection of **Python tools for GIS automation** using  
[ArcPy](https://pro.arcgis.com/en/pro-app/arcpy/) and [pandas](https://pandas.pydata.org/).  
The goal is to provide reusable scripts and ArcGIS Pro script tools for data preprocessing, analysis, and reporting.  

It is organized into **modules** (by theme), each containing scripts, examples, and documentation.  

---

## 🚀 Getting Started

### Requirements
- **ArcGIS Pro** (tested with 3.x) with ArcPy
- Python 3.9+  
- [pandas](https://pandas.pydata.org/) (see `requirements.txt`)

### Clone the repo
```bash
git clone https://github.com/<your-username>/gis-python-tools.git
cd gis-python-tools
```

### Install dependencies
```bash
pip install -r requirements.txt
```
⚠️ arcpy is not pip-installable. It is available only with ArcGIS Pro.

## 🔧 Modules

- OSM sorting & export : Export OSM layers by fclass, apply buffers, exclusions, and categorize roads.

- Change detection → Compare two layers (old vs new), generate reports.

- excel-ingest → Merge multiple Excel files and convert to CSV/SHAPE.

Each module has its own README.md with usage examples.

## 📜 License

This project is licensed under the MIT License
.
You are free to use, modify, and share it with attribution.

## 👤 Author

Jordan Metivier
Geospatial Analyst | Python & ArcGIS Automation
🔗 [LinkedIn](https://www.linkedin.com/in/jordan-m-52b404a5/)
 | [GitHub](https://github.com/jmetivier-gis/)
