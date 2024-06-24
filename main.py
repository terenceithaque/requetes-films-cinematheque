# Script qui récupère des informations sur les trimestres 
import requests # Importer le module requests pour faire des requêtes
import requests.exceptions as reqexcpt # Importer le module exceptions de requests sous le nom reqexcpt ("requests exceptions")
import datetime
import json

date_actuelle = datetime.datetime.today()
print(date_actuelle)




def get_current_date(return_string=False):
    "Obtenir la date actuelle"
    date_actuelle = datetime.datetime.today() # Obtenir la date actuelle
    if return_string: # Si on doit retourner la date sous forme de chaîne de caractères
        return str(date_actuelle) # Retourner la date sous forme de chaîne de caractères
    
    return date_actuelle # Retourner la date actuelle


def toJSON(text_data):
    "Convertir des données texte sous forme de JSON"
    donnees_json = json.loads(text_data)
    return donnees_json


    


def find_id_prog():
    "Faire une requête à l'API de la Cinémathèque et renvoyer l'ID d'un trimestre"
    try:
        global reponse # On déclare la variable reponse comme étant globale
        global donnees_json
        id_prog = 0
        reponse = requests.get("https://api.cnmtq.fr/progs") # Faire une requête de données JSON à l'API
        code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
        print("Le serveur a répondu avec le code ", code_reponse)
        texte = reponse.text # Texte contenu dans la ressource
        donnees_json = toJSON(texte) # Texte converti en JSON
        for dict in donnees_json["data"]: # Pour chaque dictionnaire correspondant à un trimestre
            #print(dict)
            id_prog = dict["id_prog"] # Identifiant du trimestre
            date_debut = dict["date_debut"][:10] # Obtenir la date de début du trimestre
            date_fin = dict["date_fin"][:10] # Obtenir la date de fin du trimestre
            #print(f"Le trismetre avec l'identifiant {id_prog} a commencé le {date_debut} et s'est terminé le {date_fin}")
            if date_actuelle > datetime.datetime.strptime(date_debut, "%Y-%m-%d") and date_actuelle < datetime.datetime.strptime(date_fin, "%Y-%m-%d"):
                print(f"Le trimestre actuel a l'ID {id_prog}")
                break

        return id_prog    

        

    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit.")    
        



def trouver_seances(id_prog, date_filter=None):
    "Trouver toutes les séances d'un trimestre ayant un ID donné"
    try:
        reponse = requests.get(f"https://api.cnmtq.fr/prog/{id_prog}/seances") # Envoyer une requête au serveur pour obtenir toutes les séances pour le trimestre ayant l'ID indiqué
        code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
        texte = reponse.text # Texte de la réponse
        donnees_json = toJSON(texte) # Convertir le texte dans un format compatible JSON
        if date_filter is not None: # Si on doit filtrer les séances par une date précise
            filtered = [seance for seance in donnees_json if seance["dateHeure"][:10] == str(date_filter)[:10]]
            return filtered

        return donnees_json
    
    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit.")    



id_prog = find_id_prog() # Envoyer une requête à l'API de la Cinémathèque

#date = datetime.datetime(2024, 7, 7)
seances = trouver_seances(id_prog, date_filter=date_actuelle) # Trouver toutes les séances pour le trimestre identifié par l'ID, filtrées par la date actuelle
print(seances)



"""
for seance in seances:
    for item in seance["items"]: 
        if "realisateurs" in item:
            print(item["titre"], f"({item["realisateurs"]})", seance["dateHeure"])
"""            