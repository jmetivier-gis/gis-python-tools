# -*- coding: utf-8 -*-
import arcpy
import os
import glob
import pandas as pd
from datetime import date
from collections import defaultdict

# ============================= FONCTIONS UTILES OSM =============================

def get_unique_fclass_values(shapefile):
    vals = set()
    with arcpy.da.SearchCursor(shapefile, ["fclass"]) as cur:
        for row in cur:
            if row[0]:
                vals.add(row[0])
    return sorted(vals)

def export_fclass_shapefiles(input_shp, output_folder, buffer_layer, exclusion_layer, prefix):
    os.makedirs(output_folder, exist_ok=True)
    for fclass in get_unique_fclass_values(input_shp):
        where = f"fclass = '{fclass}'"
        lyr = f"lyr_{prefix}_{fclass}"
        arcpy.management.MakeFeatureLayer(input_shp, lyr, where)
        arcpy.management.SelectLayerByLocation(lyr, "INTERSECT", buffer_layer, selection_type="NEW_SELECTION")
        if exclusion_layer:
            arcpy.management.SelectLayerByLocation(lyr, "INTERSECT", exclusion_layer, selection_type="REMOVE_FROM_SELECTION")
        count = int(arcpy.management.GetCount(lyr)[0])
        if count > 0:
            out_path = os.path.join(output_folder, f"{prefix}_{fclass}.shp")
            arcpy.management.CopyFeatures(lyr, out_path)
            arcpy.AddMessage(f"{os.path.basename(out_path)} exporté ({count} entités)")
        else:
            arcpy.AddMessage(f"{fclass} ignoré")
        arcpy.management.Delete(lyr)

def export_all_road_categories(roads_shp, output_folder, buffer_zone_a, buffer_zone_b, exclusion_layer):
    cats = {
        "Routes_principales": (["motorway","motorway_link","primary","primary_link","trunk","trunk_link"], buffer_zone_a),
        "Routes_secondaires": (["secondary","secondary_link"], buffer_zone_a),
        "Routes_tertiaires":  (["living_street","residential","service","tertiary","tertiary_link","unclassified"], buffer_zone_b),
    }
    for name, (fclasses, buf) in cats.items():
        where = " OR ".join([f"fclass = '{fc}'" for fc in fclasses])
        lyr = f"lyr_{name}"
        arcpy.management.MakeFeatureLayer(roads_shp, lyr, where)
        arcpy.management.SelectLayerByLocation(lyr, "INTERSECT", buf, selection_type="NEW_SELECTION")
        if exclusion_layer:
            arcpy.management.SelectLayerByLocation(lyr, "INTERSECT", exclusion_layer, selection_type="REMOVE_FROM_SELECTION")
        count = int(arcpy.management.GetCount(lyr)[0])
        if count > 0:
            out = os.path.join(output_folder, f"{name}.shp")
            arcpy.management.CopyFeatures(lyr, out)
            arcpy.AddMessage(f"{name} exportée ({count} entités)")
        else:
            arcpy.AddMessage(f"{name} ignorée")
        arcpy.management.Delete(lyr)




# ============================= FONCTIONS UTILES CHANGE DETECTION =============================


def comparer_occupations(ancienne_couche, nouvelle_couche, champ_pays, champ_type, dossier_sortie):
    # Vérification des champs
    champs_ancienne = [f.name for f in arcpy.ListFields(ancienne_couche)]
    champs_nouvelle = [f.name for f in arcpy.ListFields(nouvelle_couche)]

    champs_a_verifier = [champ_type]
    if champ_pays:
        champs_a_verifier.append(champ_pays)

    for champ in champs_a_verifier:
        if champ not in champs_ancienne:
            arcpy.AddError(f"⚠️ Le champ '{champ}' est absent de la couche ANCIENNE.")
            raise arcpy.ExecuteError
        if champ not in champs_nouvelle:
            arcpy.AddError(f"⚠️ Le champ '{champ}' est absent de la couche NOUVELLE.")
            raise arcpy.ExecuteError

    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    rapport_path = os.path.join(dossier_sortie, "rapport_changements_aires.txt")

    # Compter les entités
    nb_ancienne = int(arcpy.GetCount_management(ancienne_couche).getOutput(0))
    nb_nouvelle = int(arcpy.GetCount_management(nouvelle_couche).getOutput(0))
    diff_total_nb = nb_nouvelle - nb_ancienne

    # Utilitaire pour formater les nombres
    def fmt(x):
        return f"{x:,.2f}".replace(",", " ").replace(".", ",")

    # Calcule les aires par type (et pays si précisé)
    def sommer_aires(couche, champ_type, champ_pays=None):
        if champ_pays:
            agg = defaultdict(lambda: defaultdict(float))
            champs = [champ_pays, champ_type, "SHAPE@"]
        else:
            agg = defaultdict(float)
            champs = [champ_type, "SHAPE@"]

        with arcpy.da.SearchCursor(couche, champs) as cursor:
            for row in cursor:
                if champ_pays:
                    pays = row[0] or "Inconnu"
                    type_ = row[1] or "Non défini"
                    geom = row[2]
                else:
                    type_ = row[0] or "Non défini"
                    geom = row[1]

                if geom:
                    aire_km2 = geom.getArea("GEODESIC", "SQUAREKILOMETERS")
                else:
                    aire_km2 = 0.0

                if champ_pays:
                    agg[pays][type_] += aire_km2
                else:
                    agg[type_] += aire_km2
        return agg

    aires_ancienne = sommer_aires(ancienne_couche, champ_type, champ_pays if champ_pays else None)
    aires_nouvelle = sommer_aires(nouvelle_couche, champ_type, champ_pays if champ_pays else None)

    # Totaux d'aire
    def total_aire(agg, avec_pays):
        if avec_pays:
            return sum(sum(types.values()) for types in agg.values())
        else:
            return sum(agg.values())

    total_ancienne_km2 = total_aire(aires_ancienne, bool(champ_pays))
    total_nouvelle_km2 = total_aire(aires_nouvelle, bool(champ_pays))
    diff_total_km2 = total_nouvelle_km2 - total_ancienne_km2

    # --- Génération du rapport ---
    with open(rapport_path, "w", encoding="utf-8") as f:
        f.write("=== Rapport de comparaison des SURFACES par groupe ===\n\n")
        f.write(f"Ancienne couche : {ancienne_couche}\nNombre total d'entités : {nb_ancienne}\n")
        f.write(f"Aire totale (km²) : {fmt(total_ancienne_km2)}\n\n")

        f.write(f"Nouvelle couche : {nouvelle_couche}\nNombre total d'entités : {nb_nouvelle}\n")
        f.write(f"Aire totale (km²) : {fmt(total_nouvelle_km2)}\n\n")

        # Écart de nombre d'entités
        if diff_total_nb > 0:
            f.write(f"➡️ Entités en PLUS dans la nouvelle couche : {diff_total_nb}\n")
        elif diff_total_nb < 0:
            f.write(f"⬅️ Entités en MOINS dans la nouvelle couche : {-diff_total_nb}\n")
        else:
            f.write("✅ Nombre d'entités identique entre les deux couches.\n")

        # Écart d’aire
        signe = "📈 Gain" if diff_total_km2 >= 0 else "📉 Perte"
        f.write(f"{signe} d'aire totale : {fmt(diff_total_km2)} km²\n\n")

        # --- Comparaison détaillée dans le style demandé ---
        f.write("📊 Évolution des aires par groupe (ancienne → nouvelle, en km²) :\n\n")

        if champ_pays:
            tous_pays = set(aires_ancienne.keys()) | set(aires_nouvelle.keys())
            for pays in sorted(tous_pays):
                f.write(f"📍 {pays} :\n")
                types_anciens = aires_ancienne.get(pays, {})
                types_nouveaux = aires_nouvelle.get(pays, {})
                tous_types = set(types_anciens.keys()) | set(types_nouveaux.keys())

                for type_ in sorted(tous_types):
                    a_old = types_anciens.get(type_, 0.0)
                    a_new = types_nouveaux.get(type_, 0.0)
                    delta = a_new - a_old

                    if delta > 0:
                        symbole = "🔼"
                        signe = "+"
                    elif delta < 0:
                        symbole = "🔽"
                        signe = "-"
                    else:
                        symbole = "➖"
                        signe = ""

                    f.write(f"  - {type_} : {fmt(a_old)} → {fmt(a_new)} km² ({symbole} {signe}{fmt(abs(delta))})\n")
                f.write("\n")
        else:
            tous_types = set(aires_ancienne.keys()) | set(aires_nouvelle.keys())
            for type_ in sorted(tous_types):
                a_old = aires_ancienne.get(type_, 0.0)
                a_new = aires_nouvelle.get(type_, 0.0)
                delta = a_new - a_old

                if delta > 0:
                    symbole = "🔼"
                    signe = "+"
                elif delta < 0:
                    symbole = "🔽"
                    signe = "-"
                else:
                    symbole = "➖"
                    signe = ""

                f.write(f" - {type_} : {fmt(a_old)} → {fmt(a_new)} km² ({symbole} {signe}{fmt(abs(delta))})\n")

    arcpy.AddMessage(f"✅ Rapport généré : {rapport_path}")


# =============================== TOOLBOX UNIQUE ===============================

class Toolbox(object):
    def __init__(self):
        # Un seul label/alias pour la toolbox
        self.label = "Mes Outils Python"
        self.alias = "mes_outils"
        # Liste de TOUS les outils exposés
        self.tools = [OSMTriExport, FusionXLSX, ChangeDetection]


# ================================ OUTIL OSM ===================================

class OSMTriExport(object):
    def __init__(self):
        self.label = "OSM fclass sort & export"
        self.description = "Exporte les couches OSM par fclass avec buffers sur gabarit (Zone A) et zone d'étude (Zone B). Zone d'exclusion optionnelle."
        self.category = "OSM"
        self.canRunInBackground = True

    def getParameterInfo(self):
        p0 = arcpy.Parameter(
            displayName="Dossier dézippé contenant les fichiers OSM (.shp)",
            name="input_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        p1 = arcpy.Parameter(
            displayName="Dossier de sortie",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Output"
        )
        p2 = arcpy.Parameter(
            displayName="Gabarit",
            name="zone_a",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        p3 = arcpy.Parameter(
            displayName="Zone d'étude",
            name="zone_b",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        p4 = arcpy.Parameter(
            displayName="Buffer Gabarit (ex: 20000 Meters)",
            name="buffer_a",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )
        p5 = arcpy.Parameter(
            displayName="Buffer zone d'étude (ex: 500 Meters)",
            name="buffer_b",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )
        p6 = arcpy.Parameter(
            displayName="Emprise de la PFA (zone à exclure) (optionnel)",
            name="exclusion",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input"
        )
        p4.value = "20000 Meters"
        p5.value = "500 Meters"
        return [p0, p1, p2, p3, p4, p5, p6]

    def execute(self, parameters, messages):
        input_folder  = parameters[0].valueAsText
        output_folder = parameters[1].valueAsText
        zone_a        = parameters[2].valueAsText
        zone_b        = parameters[3].valueAsText
        buff_a        = parameters[4].valueAsText
        buff_b        = parameters[5].valueAsText
        exclusion     = parameters[6].valueAsText if parameters[6].value else None

        arcpy.env.overwriteOutput = True

        # Buffers en mémoire
        bufA = os.path.join("in_memory", "bufA")
        bufB = os.path.join("in_memory", "bufB")
        arcpy.AddMessage(f"Buffer Zone A : {buff_a}")
        arcpy.analysis.Buffer(zone_a, bufA, buff_a, dissolve_option="ALL")
        arcpy.AddMessage(f"Buffer Zone B : {buff_b}")
        arcpy.analysis.Buffer(zone_b, bufB, buff_b, dissolve_option="ALL")

        # Cartes des fichiers attendus
        layer_mapping = {
            "gis_osm_landuse_a_free_1.shp": "Landuse",
            "gis_osm_natural_a_free_1.shp": "Natural",
            "gis_osm_places_a_free_1.shp": "Places",
            "gis_osm_railways_free_1.shp": "Railways",
            "gis_osm_water_a_free_1.shp": "Waterareas",
            "gis_osm_waterways_free_1.shp": "Waterways",
        }

        # Traitement des couches surf/linéaires
        for fname, sub in layer_mapping.items():
            src = os.path.join(input_folder, fname)
            if arcpy.Exists(src):
                arcpy.AddMessage(f"Traitement: {fname}")
                out_sub = os.path.join(output_folder, sub)
                export_fclass_shapefiles(src, out_sub, bufA, exclusion, sub)
            else:
                arcpy.AddWarning(f"Fichier non trouvé: {fname}")

        # Routes
        roads = os.path.join(input_folder, "gis_osm_roads_free_1.shp")
        if arcpy.Exists(roads):
            export_all_road_categories(roads, output_folder, bufA, bufB, exclusion)
        else:
            arcpy.AddWarning("Fichier 'gis_osm_roads_free_1.shp' manquant.")

        # Nettoyage
        for tmp in (bufA, bufB):
            if arcpy.Exists(tmp):
                arcpy.management.Delete(tmp)

# =============================== OUTIL FUSION XLSX ============================

class FusionXLSX(object):
    def __init__(self):
        self.label = "XLSX merge & export (csv + shp)"
        self.description = "Fusionne des .xlsx d'un dossier, exporte un .csv et un .shp (WGS84)."
        self.category = "Tableaux"
        self.canRunInBackground = True

    def getParameterInfo(self):
        p0 = arcpy.Parameter(
            displayName="Date (préfixe AAAAMMJJ)",
            name="date_fichier",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p1 = arcpy.Parameter(
            displayName="Dossier contenant les .xlsx (servira aussi de sortie)",
            name="dossier_excel",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
            )
        p2 = arcpy.Parameter(
            displayName="Nom de la feuille",
            name="feuille",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
            )
        p3 = arcpy.Parameter(
            displayName="Champ longitude (X)",
            name="champ_x",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
            )
        p4 = arcpy.Parameter(
            displayName="Champ latitude (Y)",
            name="champ_y",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
            )

        # Valeurs par défaut (à modifier selon habitude)
        p0.value = date.today().strftime("%Y%m%d")
        p2.value = "AAAA"
        p3.value = "Longitude décimale"
        p4.value = "Latitude décimale"
        return [p0, p1, p2, p3, p4]

    def execute(self, parameters, messages):
        date_fichier  = parameters[0].valueAsText
        dossier_excel = parameters[1].valueAsText
        feuille       = parameters[2].valueAsText
        champ_x       = parameters[3].valueAsText
        champ_y       = parameters[4].valueAsText

        arcpy.env.overwriteOutput = True

        # Sorties dans le même dossier (simple et clair)
        sortie_csv = os.path.join(dossier_excel, f"{date_fichier}_fusion.csv")
        sortie_shp = os.path.join(dossier_excel, f"{date_fichier}_fusion.shp")

        arcpy.AddMessage("Recherche des fichiers Excel dans : " + dossier_excel)
        fichiers = glob.glob(os.path.join(dossier_excel, "*.xlsx"))
        if not fichiers:
            raise arcpy.ExecuteError("Aucun fichier Excel (.xlsx) trouvé dans le dossier spécifié.")

        arcpy.AddMessage(f"{len(fichiers)} fichiers trouvés.")

        # Fusion xlsx
        df_combined = pd.concat(
            [pd.read_excel(fichier, sheet_name=feuille) for fichier in fichiers],
            ignore_index=True
        )

        # Vérifier les champs
        if champ_x not in df_combined.columns or champ_y not in df_combined.columns:
            raise arcpy.ExecuteError(f"Champs '{champ_x}' et/ou '{champ_y}' absents dans les Excel.")

        # Export CSV
        df_combined.to_csv(sortie_csv, index=False)
        arcpy.AddMessage(f"CSV exporté : {sortie_csv}")

        # Points (WGS84)
        arcpy.management.XYTableToPoint(
            in_table=sortie_csv,
            out_feature_class=sortie_shp,
            x_field=champ_x,
            y_field=champ_y,
            coordinate_system=arcpy.SpatialReference(4326)
        )
        arcpy.AddMessage(f"Shapefile créé : {sortie_shp}")

# ================================ OUTIL CHANGE DETECTION ===================================

class ChangeDetection(object):
    def __init__(self):
        self.label = "Change detection"
        self.description = "Permet de faciliter la comparaison entre un vecteur surfacique et sa mise à jour. L'outil génère un rapport au format txt des évolutions des aires des entités entre les deux fichiers en entrée."
        self.category = "Change detection"
        self.canRunInBackground = True

    def getParameterInfo(self):
        p0 = arcpy.Parameter(
            displayName="Ancienne couche",
            name="ancienne_couche",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        p1 = arcpy.Parameter(
            displayName="Nouvelle couche",
            name="nouvelle_couche",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        p2 = arcpy.Parameter(
            displayName="Champ pays (optionnel)",
            name="champ_pays",
            datatype="Field",
            parameterType="Optional",
            direction="Input"
        )
        p2.parameterDependencies = ["ancienne_couche"]
        #p2.filter.list = ["String", "SmallInteger", "Integer"]

        p3 = arcpy.Parameter(
            displayName="Champ type",
            name="champ_type",
            datatype="Field",
            parameterType="Required",
            direction="Input"
        )
        p3.parameterDependencies = ["ancienne_couche"]
        #p3.filter.list = ["String", "SmallInteger", "Integer"]

        p4 = arcpy.Parameter(
            displayName="Dossier de sortie",
            name="dossier_sortie",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        return [p0, p1, p2, p3, p4]

    #def updateParameters(self, parameters):
        #ancienne = parameters[0].value
        #if ancienne:
            #try:
                #champs = [f.name.lower() for f in arcpy.ListFields(ancienne.value)]

                # Pré-remplissage auto
                #if "pays" in champs and not parameters[2].value:
                    #parameters[2].value = [f.name for f in arcpy.ListFields(ancienne.value) if f.name.lower() == "pays"][0]

                #if "type" in champs and not parameters[3].value:
                    #parameters[3].value = [f.name for f in arcpy.ListFields(ancienne.value) if f.name.lower() == "type"][0]

            #except Exception as e:
                #arcpy.AddWarning(f"Erreur lors de la lecture des champs : {str(e)}")

    def execute(self, parameters, messages):
        ancienne_couche = parameters[0].valueAsText
        nouvelle_couche = parameters[1].valueAsText
        champ_pays = parameters[2].valueAsText if parameters[2].value else None
        champ_type = parameters[3].valueAsText
        dossier_sortie = parameters[4].valueAsText

        arcpy.env.overwriteOutput = True
        comparer_occupations(ancienne_couche, nouvelle_couche, champ_pays, champ_type, dossier_sortie)
