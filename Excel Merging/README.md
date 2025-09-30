# Excel Merging → CSV & Shapefile (ArcPy + pandas)

## 📌 Description
This tool merges **all `.xlsx` files** from a given folder into a single CSV, then converts it to a **point shapefile** using longitude/latitude columns.  
The output filenames are **timestamped** via a user-provided date string (e.g., `2025-09-30_AAAA.csv` / `.shp`). The script expects **fixed folders** for inputs and outputs, a **fixed sheet name** (`"AAAA"`), and **fixed coordinate fields** (`"Longitude décimale"`, `"Latitude décimale"`).

---

## ⚙️ Requirements
- **ArcGIS Pro** (ArcPy bundled)  
- **Python 3.9+**  
- Python packages: `pandas`, `openpyxl` (engine used by pandas to read `.xlsx`)  

> Example `requirements.txt` at repo root:
> ```
> pandas>=2.0.0
> openpyxl>=3.1.0
> # arcpy (bundled with ArcGIS Pro)
> ```

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
