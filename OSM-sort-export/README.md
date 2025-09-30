# OSM-sort-export (arcpy)

## 📌 Description
This repository contains a Python script (`osm-sort-export.py`) designed to **automatically process and export OpenStreetMap (OSM) shapefiles** by `fclass`.  
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
1. **Input folder**: path to the OSM shapefiles  
2. **Output folder**: destination for the processed shapefiles  
3. **Zone A layer**: buffer base for all categories except tertiary roads  
4. **Zone B layer**: buffer base for tertiary roads only  
5. **Buffer A distance**  
6. **Buffer B distance**  
7. **Exclusion layer** (optional)  

---

## 📂 Example Workflow
```bash
python tri_osm.py "C:\Data\OSM" "C:\Data\Output" zoneA.shp zoneB.shp 200m 100m exclusion_zone.shp
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



