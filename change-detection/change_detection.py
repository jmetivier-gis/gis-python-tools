import arcpy
import os
from collections import defaultdict

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


# === Pour exécution dans ArcGIS Pro ===
if __name__ == "__main__":
    ancienne = arcpy.GetParameterAsText(0)
    nouvelle = arcpy.GetParameterAsText(1)
    champ_pays = arcpy.GetParameterAsText(2)
    champ_type = arcpy.GetParameterAsText(3)
    dossier_sortie = arcpy.GetParameterAsText(4)

    comparer_occupations(ancienne, nouvelle, champ_pays, champ_type, dossier_sortie)
