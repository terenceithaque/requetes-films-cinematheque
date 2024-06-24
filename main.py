# Script qui récupère des informations sur les trimestres 
import requests # Importer le module requests pour faire des requêtes
import requests.exceptions as reqexcpt # Importer le module exceptions de requests sous le nom reqexcpt ("requests exceptions")
import datetime
import json

print(datetime.datetime.today())


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

def make_request():
    "Faire une requête à l'API de la Cinémathèque"
    try:
        reponse = requests.get("https://api.cnmtq.fr/progs") # Faire une requête de données JSON à l'API
        code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
        print("Le serveur a répondu avec le code ", code_reponse)
        texte = reponse.text # Texte contenu dans la ressource
        donnees_json = toJSON(texte) # Texte converti en JSON
        for cle in donnees_json:
            print(cle, ":", donnees_json[cle])

    except reqexcpt.ConnectionError: # En cas d'erreur de connection
        print("Impossible de se connecter au serveur.")

    except reqexcpt.Timeout: # Si la requête a expiré
        print("La requête n'a pas aboutit.")    
        



make_request() # Envoyer une requête à l'API de la Cinémathèque