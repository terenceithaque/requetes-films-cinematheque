# Script qui récupère des informations sur les trimestres 
import requests # Importer le module requests pour faire des requêtes

def make_request():
    "Faire une requête à l'API de la Cinémathèque"
    reponse = requests.get("https://api.cnmtq.fr/progs") # Faire une requête de données JSON à l'API
    code_reponse = reponse.status_code # Code de la réponse (par exemple, 200)
    print("Le serveur a répondu avec le code ", code_reponse)
    if code_reponse == 404: # Si le serveur indique que la ressource est introuvable
        raise Exception(print(f"Le serveur n'a pas réussi a trouver la ressource demandée (code d'erreur : {code_reponse}) "))
    
    elif code_reponse == 200: # Si la ressource demandée a été trouvée
        print(reponse.text) # Afficher le contenu de la réponse



make_request() # Envoyer une requête à l'API de la Cinémathèque