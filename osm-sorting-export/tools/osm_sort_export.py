import arcpy
import os
import glob
import pandas as pd

def main():
    date_fichier=arcpy.GetParameterAsText(0)
    
    # Chemin fixe vers dossier des fichiers Excel
    dossier_excel = r"C:\Chemin\de\fichier\AAAA"

    # Chemin fixe vers dossier de sortie
    dossier_sortie_csv = r"C:\Chemin\de\fichier\AAAA CSV"
    dossier_sortie_shp = r"C:\Chemin\de\fichier\AAAA SHP"
    
    # Nom fixe de la feuille Excel
    feuille = "AAAA"

    # Champs fixes pour coordonnées
    champ_x = "Longitude décimale"
    champ_y = "Latitude décimale"

    # Chemins fixes des fichiers de sortie
    sortie_csv = os.path.join(dossier_sortie_csv, f"{date_fichier}_AAAA.csv")
    sortie_shp = os.path.join(dossier_sortie_shp, f"{date_fichier}_AAAA.shp")

    arcpy.AddMessage("Recherche des fichiers Excel dans : " + dossier_excel)
    fichiers = glob.glob(os.path.join(dossier_excel, "*.xlsx"))
    if not fichiers:
        raise arcpy.ExecuteError("Aucun fichier Excel (.xlsx) trouvé dans le dossier spécifié.")

    arcpy.AddMessage(f"{len(fichiers)} fichiers trouvés.")

    # Fusionner les Excel
    df_combined = pd.concat(
        [pd.read_excel(fichier, sheet_name=feuille) for fichier in fichiers],
        ignore_index=True
    )

    # Vérifier les champs
    if champ_x not in df_combined.columns or champ_y not in df_combined.columns:
        raise arcpy.ExecuteError(f"Les champs '{champ_x}' et/ou '{champ_y}' ne sont pas présents.")

    # Export CSV
    df_combined.to_csv(sortie_csv, index=False)
    arcpy.AddMessage(f"CSV exporté : {sortie_csv}")

    # Créer shapefile
    arcpy.env.overwriteOutput = True
    arcpy.management.XYTableToPoint(
        in_table=sortie_csv,
        out_feature_class=sortie_shp,
        x_field=champ_x,
        y_field=champ_y,
        coordinate_system=arcpy.SpatialReference(4326)
    )
    arcpy.AddMessage(f"Shapefile créé : {sortie_shp}")

if __name__ == "__main__":
    main()
