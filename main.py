# Script qui récupère des informations sur les trimestres 
import requests # Importer le module requests pour faire des requêtes
import requests.exceptions as reqexcpt # Importer le module exceptions de requests sous le nom reqexcpt ("requests exceptions")
import datetime
import json
import sys
import os
import re




date_actuelle = datetime.datetime.today() # Obtenir la date actuelle afin de déterminer quel est le trimestre actuel
print(date_actuelle)




"""def get_current_date(return_string=False):
    "Obtenir la date actuelle"
    date_actuelle = datetime.datetime.today() # Obtenir la date actuelle
    if return_string: # Si on doit retourner la date sous forme de chaîne de caractères
        return str(date_actuelle) # Retourner la date sous forme de chaîne de caractères
    
    return date_actuelle # Retourner la date actuelle"""

def convertir_date_formatee(date_formatee=str(date_actuelle)):
    "Convertir une date formatée dans une date lisible"
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
    
    annee_formatee, mois_formate,jour_formate = date_formatee.split("-")[0], date_formatee.split("-")[1], date_formatee.split("-")[2] # Année, mois et jours formaté contenus dans la date
    
    jour_affiche = jour_formate[:3].replace("T", "")# Jour tel qu'il est affiché dans la date lisible
    heure = jour_formate[3:]  # Heure dans le jour
    

    for m in mois:
        if mois[m] == mois_formate:
            mois_affiche = m

    annee_affichee = annee_formatee # Année telle qu'affichée dans la date lisible

    return f"{jour_affiche} {mois_affiche} {annee_affichee} à {heure}"



    



    
    

def enregistrer_donnees(donnees, date=date_actuelle):
    "Enregistrer des données dans un fichier JSON"

    date = re.sub(r"\W+", "-", date.strftime('%Y-%m-%d_%H-%M-%S')) # Enlever les caractères interdits de la date

    with open(f"seances_cinematheque_{date}.json", "w") as f: # Ouvrir le fichier seances.json en écriture
        json.dump(donnees, f, indent=4)
        f.close()
        print(f"Les séances ont été enregistrées dans {os.path.abspath(f"seances_{date}.json")}")


def toJSON(text_data):
    "Convertir des données texte sous forme de JSON"
    donnees_json = json.loads(text_data)
    return donnees_json


def minutes_en_heures(minutes=60):
    "Convertir le temps d'une séance de minutes en heures"
    heures = minutes // 60 # Calculer le nombre d'heures en faisant une division entière de la séance en minutes
    minutes_restantes = minutes % 60 # Rajouter le nombre de minutes restantes au nombre d'heures
    return (heures, minutes_restantes)
    


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
    "Trouver toutes les séances d'un trimestre ayant un ID donné"
    try:
        reponse = requests.get(f"https://api.cnmtq.fr/prog/{id_prog}/seances") # Envoyer une requête au serveur pour obtenir toutes les séances pour le trimestre ayant l'ID indiqué
        code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
        texte = reponse.text # Texte de la réponse
        donnees_json = toJSON(texte) # Convertir le texte dans un format compatible JSON
        filtered = [] # Données filtrées
        if date_filter is not None: # Si on doit filtrer les séances par une date précise
            
            #print("Séance :", seance)
            filtered = [seance for seance in donnees_json if seance["dateHeure"][:10] == str(date_filter)[:10]]
            #print("Séances filtrées par date :", filtered)
            return filtered
        
        elif other_filter is not None:
                for seance in donnees_json: # Pour chaque séance
                        for cle, valeur in seance.items():
                            print("Clé :", cle)
                            print("Valeur :",valeur)
                            if str(cle)==other_filter or other_filter in str(cle) or str(valeur)==other_filter or other_filter in str(valeur):
                                filtered.append(seance)
                                #print(f"Séances filtrées par {other_filter}", filtered)
                
                return filtered
        
        


        
        
        
        
        

            
                    
        



        return donnees_json
    
    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit car le serveur a mis trop de temps à répondre.")    







date = date_actuelle
filtre = None # Filtre que l'utilisateur peut appliquer pour trouver uniquement certaines séances
save = False # Variable pour déterminer s'il faut enregistrer les données dans un fichier
for arg in sys.argv: # Pour chaque argument donné au script
    if arg.startswith("date_filter=") and arg.split("=")[1]: # Si l'argument spécifie le filtre des séances par années
        date = datetime.datetime.strptime(arg[12:], "%Y-%m-%d")


    if arg.startswith("filter=") and arg.split("=")[1:]: # Si l'argument indique qu'il faut appliquer un autre filtre
        filtre = "".join(arg.split("=")[1:])
        date = None
        
    if arg == "save": # Si l'argument indique qu'il faut enregistrer
        save = True 


    
    


id_prog = find_id_prog() # Envoyer une requête à l'API de la Cinémathèque
        
    


seances = trouver_seances(id_prog, date_filter=None, other_filter=filtre) # Trouver toutes les séances pour le trimestre identifié par l'ID, filtrées par la date actuelle




if len(seances) > 0:
    print(f"Les séances suivantes ont été programmées pour la date du {date} :")
    print() # Faire un saut à la ligne
    for seance in seances:
        for item in seance["items"]:
            #print(item)

            try:

                duree = minutes_en_heures(item["duree"]) # Durée de la séance convertie en heures
                heures = duree[0] # Durée en heures
                minutes = duree[1] # Durée en minutes
                if "realisateurs" in item:
                    print("Titre :", item["titre"],f"({item["annee"]})",  ", Realisateur(s) :", f"{item["realisateurs"]}", ", Horaires de la séance :", convertir_date_formatee(seance["dateHeure"]), f", Durée de la séance : {heures} heure(s) {minutes} minutes")

                else:
                 print("Titre :", item["titre"], f"({item["annee"]})", ", Horaires de la séance :", convertir_date_formatee(seance["dateHeure"]), f", Durée de la séance : {heures} heures {minutes} minutes")

            except KeyError:
                continue

    if save: # S'il faut enregistrer les séances dans un fichier
        enregistrer_donnees(seances, date=date if date is not None else date_actuelle)

else:
        print(f"Aucune séance n'a été programmée pour la date du {convertir_date_formatee(str(date))}")

    



            