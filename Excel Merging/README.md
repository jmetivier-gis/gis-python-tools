# Excel Merging → CSV & Shapefile (ArcPy + pandas)

## 📌 Description
This module provides a Python script (`fusion_xlsx.py`) to **merge multiple Excel files** into a single dataset and export it to both **CSV and Shapefile** formats.  

The script:
- Reads all `.xlsx` files from a fixed input folder  
- Uses a fixed sheet name (`"AAAA"`)  
- Concatenates rows into one combined table  
- Writes the output to a timestamped CSV and Shapefile  
- Creates point features based on `Longitude décimale` and `Latitude décimale` columns (WGS84 / EPSG:4326)

Output files are automatically named with the provided date parameter, e.g.:
- `2025-09-30_AAAA.csv`
- `2025-09-30_AAAA.shp`

---

## ⚙️ Requirements
- **ArcGIS Pro** (ArcPy bundled)  
- **Python 3.9+**  
- Python packages: `pandas`, `openpyxl` (engine used by pandas to read `.xlsx`)  

---

## 🧰 Parameters & Assumptions

| Parameter (order) | Meaning                             | Type                                        | Example                      |
|-------------------|-------------------------------------|---------------------------------------------|------------------------------|
| 1) `date_fichier` | Date tag used in output filenames   |    String                                    | `2025-09-30`                 |

**Fixed settings inside the script** (edit to fit your environment):  
- Input Excel folder: `C:\Chemin\de\fichier\AAAA`  
- Output CSV folder: `C:\Chemin\de\fichier\AAAA CSV`  
- Output SHP folder: `C:\Chemin\de\fichier\AAAA SHP`  
- Excel sheet name: `AAAA`  
- X field: `Longitude décimale`  
- Y field: `Latitude décimale`

---

## 🚀 Usage

### As an ArcGIS Pro Script Tool
1. Add the script to a Toolbox (Right click **Toolbox** → **Add** → **Script**).  
2. Map the single parameter **Date** (`date_fichier`).  
3. Run. The tool will:
   - read every `*.xlsx` in the input folder, sheet `"AAAA"`,  
   - **concatenate** rows,  
   - write a CSV to `AAAA CSV\{date}_AAAA.csv`,  
   - create a **point shapefile** to `AAAA SHP\{date}_AAAA.shp` (WGS84 / EPSG:4326).

### From an ArcPy-enabled Python
```bash
python fusion_xlsx.py 2025-09-30
```
## 📂 Outputs

- C:\Chemin\de\fichier\AAAA CSV\{date}_AAAA.csv

- C:\Chemin\de\fichier\AAAA SHP\{date}_AAAA.shp
Coordinates interpreted as WGS84 (EPSG:4326).

## ✅ Validations & Errors

- Fails early if no *.xlsx is found in the input folder.

- Fails if the columns Longitude décimale or Latitude décimale are missing in merged data.

- Overwrite is enabled for the shapefile creation step.

💡 Tips / Improvements (optional)

- Replace fixed Windows paths by tool parameters (input/output folders).

- Make sheet_name, x_field, y_field configurable.

- Add a quick schema check (e.g., numeric X/Y; drop rows with nulls).

- Optionally output file geodatabase (.gdb) instead of shapefile.

## 👤 Author

Jordan Metivier — GIS Analyst & Python/ArcPy Developer
🔗 [GitHub](https://github.com/jmetivier-gis)

## 📜 License

MIT — free to use, modify, and distribute.
