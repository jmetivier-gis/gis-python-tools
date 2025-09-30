# OSM-sort-export (arcpy)

## 📌 Description
This repository contains a Python script (`osm_sort_export.py`) designed to **automatically process and export OpenStreetMap (OSM) shapefiles** by `fclass`.  
The script uses **ArcPy** to:
- Extract unique `fclass` values from OSM layers  
- Apply spatial filters with **buffers** and **exclusion zones**  
- Export the results into separate shapefiles per category (landuse, natural, places, railways, water, roads, etc.)  
- Handle road layers in 3 categories (primary, secondary, tertiary) with specific buffer rules  

This tool helps streamline repetitive OSM preprocessing tasks for GIS workflows.

---

## ⚙️ Requirements
- **ArcGIS Pro** (tested with 3.x)  
- **ArcPy** Python library  
- Input OSM shapefiles (e.g. from [Geofabrik](https://download.geofabrik.de/))  

---

## 🚀 Usage
Run the script from ArcGIS Pro (Toolbox) or directly in Python with ArcPy.

### Parameters
| Parameter        | Description                                        | Type   |
|------------------|----------------------------------------------------|--------|
| Input folder     | Path to the OSM shapefiles                         | Folder |
| Output folder    | Destination for the processed shapefiles           | Folder |
| Zone A layer     | Buffer base for all categories except tertiary     | Layer  |
| Zone B layer     | Buffer base for tertiary roads only                | Layer  |
| Buffer A dist.   | Distance for Zone A buffer                         | Value  |
| Buffer B dist.   | Distance for Zone B buffer                         | Value  |
| Exclusion layer  | Optional layer to exclude from the results         | Layer  |

---

## 📂 Example Workflow
```bash
python osm_sort_export.py "C:\Data\OSM" "C:\Data\Output" zoneA.shp zoneB.shp 200m 100m exclusion_zone.shp
```

Resulting structure:
```
Output/
 ├── Landuse/
 ├── Natural/
 ├── Places/
 ├── Railways/
 ├── Waterareas/
 ├── Waterways/
 ├── Routes principales.shp
 ├── Routes secondaires.shp
 └── Routes tertiaires.shp
```

## 🧑‍💻 Author

Jordan Metivier – GIS analyst & Python/ArcPy developer
🔗 [GitHub](https://github.com/jmetivier-gis)


## 📜 License

MIT License – free to use, modify and distribute.



