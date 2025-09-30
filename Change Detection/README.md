# Change Detection Tools (ArcPy)

## 📌 Description
This module provides a Python script (`change_detection.py`) to **compare two versions of a GIS dataset**  
(e.g., old vs. new occupation layers) and generate a **report of changes**.  

It is useful to track dataset updates and document:
- Differences in the number of features
- Entities added or removed
- Distribution of types (and optionally by country)
- A text-based report summarizing all changes

---

## ⚙️ Requirements
- **ArcGIS Pro** (tested with 3.x)  
- **ArcPy** Python library  

---

## 🚀 Usage
Run the script as a **Script Tool in ArcGIS Pro** or directly with Python/ArcPy.

### Parameters
| Parameter         | Description                                                                 | Type   |
|-------------------|-----------------------------------------------------------------------------|--------|
| Old layer         | Path to the *old* dataset                                                   | Layer  |
| New layer         | Path to the *new* dataset                                                   | Layer  |
| Country field     | (Optional) Field name with the country attribute (e.g., `"COUNTRY"`)        | String |
| Type field        | Field name with the type/class attribute (e.g., `"TYPE"` or `"FACTION"`)    | String |
| Output folder     | Folder where the comparison report (`rapport_changements.txt`) will be saved | Folder |

---

## 📂 Example Workflow
```bash
python change_detection.py "data/old_layer.shp" "data/new_layer.shp" COUNTRY TYPE ./output

