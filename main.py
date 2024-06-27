"Convertir du JSON dans un tableau au format CSV"
# Script principal
import json
import requests
import requests.exceptions as reqexcpt # Importer le module exceptions de requests sous le nom reqexcpt ("requests exceptions")
import csv
import pandas
from io import StringIO
import sys
import datetime
import re
import os


date_actuelle = datetime.datetime.today() # Date actuelle

args = sys.argv # Liste des paramètres donnés au script

def convertir_date_formatee(date_formatee=str(date_actuelle)):
    "Convertir une date formatée dans une date lisible"
    if date_formatee is None:
        date = str(date_actuelle)
    print("Date formatée :", date_formatee)
    date = "" # Date finale, lisible

    jours_par_mois = {"janvier":31,
                      "février":29,
                      "mars":31,
                      "avril":30,
                      "mai":31,
                      "juin":30,
                      "juillet":31,
                      "août":31,
                      "septembre":30,
                      "octobre":31,
                      "novembre":30,
                      "decembre":31
                     } # Dictionnaire du nombre de jours par mois
    
    mois = {"janvier":"01",
            "février":"02",
            "mars":"03",
            "avril":"04",
            "mai":"05",
            "juin":"06",
            "juillet":"07",
            "août":"08",
            "septembre":"09",
            "octobre":"10",
            "novembre":"11",
            "decembre":"12"} # Dictionnaire du nombre de mois par années
    try:
        annee_formatee, mois_formate,jour_formate = date_formatee.split("-")[0], date_formatee.split("-")[1], date_formatee.split("-")[2] # Année, mois et jours formaté contenus dans la date
        jour_affiche = jour_formate[:3].replace("T", "")# Jour tel qu'il est affiché dans la date lisible
        heure = jour_formate[3:]  # Heure dans le jour
    

        for m in mois:
            if mois[m] == mois_formate:
                mois_affiche = m

        annee_affichee = annee_formatee # Année telle qu'affichée dans la date lisible

        return f"{jour_affiche} {mois_affiche} {annee_affichee} à {heure} heures"
    
    except IndexError as e:
        print(f"Erreur lors de la conversion de la date {date}: {e}")
        







def minutes_en_heures(minutes=60):
    "Convertir le temps d'une séance de minutes en heures"
    heures = minutes // 60 # Calculer le nombre d'heures en faisant une division entière de la séance en minutes
    minutes_restantes = minutes % 60 # Rajouter le nombre de minutes restantes au nombre d'heures
    return (heures, minutes_restantes)

def toJSON(text_data):
    "Convertir des données texte sous forme de JSON"
    donnees_json = json.loads(text_data)
    return donnees_json


def find_id_prog(date=date_actuelle):
    "Faire une requête à l'API de la Cinémathèque et renvoyer l'ID d'un trimestre"
    try:
        global reponse # On déclare la variable reponse comme étant globale
        global donnees_json
        id_prog = 0
        reponse = requests.get("https://api.cnmtq.fr/progs") # Faire une requête de données JSON à l'API
        code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
        print("Le serveur a répondu avec le code ", code_reponse) # Afficher le code renvoyé par le serveur
        texte = reponse.text # Texte contenu dans la ressource
        donnees_json = toJSON(texte) # Texte converti en JSON
        for dict in donnees_json["data"]: # Pour chaque dictionnaire correspondant à un trimestre
            #print(dict)
            id_prog = dict["id_prog"] # Identifiant du trimestre
            date_debut = dict["date_debut"][:10] # Obtenir la date de début du trimestre
            date_fin = dict["date_fin"][:10] # Obtenir la date de fin du trimestre
                #print(f"Le trismetre avec l'identifiant {id_prog} a commencé le {date_debut} et s'est terminé le {date_fin}")
            if date > datetime.datetime.strptime(date_debut, "%Y-%m-%d") and date < datetime.datetime.strptime(date_fin, "%Y-%m-%d"): # Si la date actuelle est comprise entre la date début et la date de fin du trimestre
                print(f"Le trimestre actuel a l'ID {id_prog}") # On en déduit l'identifiant est celui du trimestre actuel
                break # Une fois l'identifiant du trimestre actuel trouvé, quitter la boucle

        return id_prog # Retourner l'identifiant du trimestre actuel
        
          


                

    
    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit car le serveur a mis trop de temps à répondre.")    

def trouver_seances(id_prog, date_filter=None, other_filter=None):
    "Récupérer le JSON depuis l'API de la Cinémathèque"
    try:
        reponse = requests.get(f"https://api.cnmtq.fr/prog/{id_prog}/seances")  # Demander le programme actuel (actuellement 179)
        code_reponse = reponse.status_code # Code renvoyé par le serveur (par exemple, 200)
        texte_reponse = reponse.text # Obtenir le texte de la réponse
        donnees_json = json.loads(texte_reponse) # Convertir le texte de la réponse en JSON
        filtered = [] # Liste des séances filtrées

        if date_filter is not None and other_filter is not None: # Si l'utilisateur a appliqué un filtre de date et un autre filtre
            filtered = [seance for seance in donnees_json if seance["dateHeure"][:10] == str(date_filter)[:10]] # Filtrer les séances par date
            for seance in filtered:
                
                filtered = [seance for i, seance in enumerate(filtered) 
                            if  any((str(cle)==other_filter or other_filter in str(cle) or str(valeur)==other_filter or other_filter in str(valeur)) 
                            for cle, valeur in seance.items())] # Filtrer à nouveau les séances selon l'autre filtre donné
                    
                print(f"Séances filtrées par date et {other_filter}:", filtered)
                  

                return filtered                    

        elif date_filter is not None: # Si on doit filtrer les séances par une date précise
            
            #print("Séance :", seance)
            filtered = [seance for seance in donnees_json if seance["dateHeure"][:10] == str(date_filter)[:10]]
            print(f"Séances filtrées par {date_filter}:", filtered)
            #print("Séances filtrées par date :", filtered)
            return filtered
        
        elif other_filter is not None:
                for seance in donnees_json: # Pour chaque séance
                            for cle, valeur in seance.items():
                                print("Clé :", cle)
                                print("Valeur :",valeur)
                                if str(cle)==other_filter or other_filter in str(cle) or str(valeur)==other_filter or other_filter in str(valeur):
                                    filtered.append(seance)
                                    break # Quitter la boucle afin d'éviter les doublons

                                #print(f"Séances filtrées par {other_filter}", filtered)

                return filtered

                    #print(f"Séances filtrées par {other_filter}:", filtered)            
                
                

                              


                        
        
        """elif other_filter is not None and date_filter is None:
            filtered = [seance for i, seance in enumerate(filtered) 
                            if  any((str(cle)==other_filter or other_filter in str(cle) or str(valeur)==other_filter or other_filter in str(valeur)) 
                            for cle, valeur in seance.items())]

            return filtered"""
        
        return donnees_json

    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit car le serveur a mis trop de temps à répondre.") 


def clean_json(data):
    "Renvoie un objet correspondant à du JSON `[{ titre, realisateurs, annee, dateHeure, duree }, ...]`"
    liste_items = ["titre", "realisateurs", "annee", "duree"] # Liste des items à récupérer
    donnees_json = [] # Objet json qui contiendra les données  
    for seance in data: # Pour chaque séance
        json_filtre = {}
        
        for item in seance["items"]:
            for cle, valeur in item.items(): # Pour chaque clé et valeur du dictionnaire item
                if cle in liste_items: # Si la clé actuelle fait partie des items à garder
                    if cle == "duree": # Si la clé spécifie la durée en minutes de la séance
                        duree = minutes_en_heures(valeur) # Durée convertie en heures et minutes
                        heures = duree[0] # Durée en heures
                        minutes = duree[1] # Durée en minutes
                        json_filtre[cle] = f"{heures}h{minutes} minutes" # Ajouter la durée convertie en heures et minutes au JSON

                    else: # Si la clé spécifie autre chose    
                        json_filtre[cle] = valeur
        
        json_filtre["dateHeure"] = convertir_date_formatee(seance["dateHeure"])   
        donnees_json.append(json_filtre)
    return donnees_json                    

def toCSV(data, date=date_actuelle):
    "Convertir les données au format CSV"
    date = re.sub(r"\W+", "-", date.strftime('%Y-%m-%d_%H-%M-%S')) # Enlever les caractères interdits de la date
    data = json.dumps(data)
    donnees_json = pandas.read_json(StringIO(data))
    file = f"seances_{date}.csv"
    donnees_json.to_csv(file, encoding="utf-8", index=False)
    print(f"Les séances du {convertir_date_formatee(str(date))} ont été enregistrées dans {os.path.abspath(file)} ")


# Code principal, point d'entrée du script


date = None 
filter = None # Filtre que l'utilisateur peut appliquer pour trouver des séances spécifiques

for arg in args: # Pour chaque argument donné au script
    if arg.startswith("date_filter=") and arg.split("=")[1]: # Si l'argument spécifie le filtre des séances par années
        date = datetime.datetime.strptime(arg[12:], "%Y-%m-%d")
    if arg.startswith("filter=") and arg.split("=")[1:]: # Si l'argument indique qu'il faut appliquer un autre filtre
        filter = "".join(arg.split("=")[1:])
            

id_prog = find_id_prog(date_actuelle) 
seances = trouver_seances(id_prog, date_filter=date, other_filter=filter)
print("seances n'est pas None")
if len(seances) > 0: # Si des séances ont été trouvées selon les différents filtres
    seances = clean_json(seances)
    toCSV(seances, date=date if date is not None else date_actuelle)

else:
    print(f"Aucune séance n'a été trouvée pour la date du {convertir_date_formatee(str(date))}")    




