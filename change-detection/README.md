# Change Detection Tools (ArcPy)

## 📌 Description
This module provides a Python script (`change_detection.py`) to **compare two versions of a GIS dataset**  
(e.g., old vs. new occupation layers) and generate a **report of changes** summarizing:
- Total feature counts (delta old → new)
- **Geodesic area** totals (km²) for each group
- Detailed **per-group** evolution (old → new, delta with up/down symbols)
- Optional breakdown **by country** (if a country field is provided)

The script computes areas with ArcPy using **geodesic** measurements in **square kilometers**, ensuring consistent results across projections.  
Output file: `rapport_changements_aires.txt` 

---

## ⚙️ Requirements
- **ArcGIS Pro** (tested with 3.x)  
- **ArcPy** Python library  

---

## 🚀 Usage
### As an ArcGIS Pro Script Tool
1. Add the Python script to a Toolbox (Right Click → **Add** → **Script**).  
2. Map the parameters in the same order as under.  
3. Run the tool; the report path is printed as a message when finished.

### From the command line (ArcPy environment)
```bash
python change_detection.py "data/old_layer.shp" "data/new_layer.shp" COUNTRY TYPE ./output

```

### Parameters
| Parameter         | Description                                                                 | Type   |
|-------------------|-----------------------------------------------------------------------------|--------|
| Old layer         | Path to the *old* dataset                                                   | Layer  |
| New layer         | Path to the *new* dataset                                                   | Layer  |
| Country field     | (Optional) Field name with the country attribute (e.g., `"COUNTRY"`)        | String |
| Type field        | Field name with the type/class attribute (e.g., `"CLASS"`)                   | String |
| Output folder     | Folder where the comparison report (`rapport_changements_aires.txt`) will be saved | Folder |

---

## 📂 Example output (rapport_changements_aires.txt)
```
=== Rapport de comparaison des SURFACES par groupe ===

Ancienne couche : old_layer.shp
Nombre total d'entités : 1200
Aire totale (km²) : 12 345,67

Nouvelle couche : new_layer.shp
Nombre total d'entités : 1345
Aire totale (km²) : 12 890,10

➡️ Entités en PLUS dans la nouvelle couche : 145
📈 Gain d'aire totale : 544,43 km²

📊 Évolution des aires par groupe (ancienne → nouvelle, en km²) :

📍 France :
  - Type A : 250,00 → 260,50 km² (🔼 +10,50)
  - Type B : 120,00 → 118,00 km² (🔽 -2,00)

📍 Germany :
  - Type A : 300,00 → 320,00 km² (🔼 +20,00)
  - Type C : 180,00 → 190,00 km² (🔼 +10,00)
```

## 📁 Files

change_detection.py — main script (ArcPy), generates the report.

Validates required fields, computes counts & geodesic areas, formats numbers, writes per-group deltas.

## ⚠️ Limitations & tips

- Ensure both layers contain the specified Type field (and Country field if used), otherwise the tool raises an ArcPy error.

- For polygon inputs with mixed or invalid geometries, repair geometry first.

- Results are geodesic (km²), independent of layer projection; avoid mixing datasets with wildly inconsistent geometry validity.

## 👤 Author

Jordan Metivier — GIS Analyst & Python/ArcPy Developer
🔗 [GitHub](https://github.com/jmetivier-gis)

## 📜 License

MIT — free to use, modify, and distribute.


