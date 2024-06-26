Ce programme sert à trouver les séances programmées à la Cinémathèque pour le trimestre actuel, et permet également de filtrer ces séances par date.

Il est possible de fournir des arguments dans une console lors de l'exécution afin de modifier les résultats obtenus:

    -> date_filter: Demande de n'afficher que les séances qui ont lieu à un jour précis. La date fournie doit être sous la forme annee-numero_mois-numero_jour. Par     exemple, pour afficher les séances du 11 juillet 2024, il faut saisir date_filter=2024-07-11.

    -> filter: Filtre les films selon un contenu spécifié. Par exemple, pour afficher uniquement les films de James Cameron, il faut saisir filter=James Cameron.

    -> save: Si ce mot-clé est fourni, alors le programme va enregistrer toutes les séances sur le disque dur dans un fichier au format JSON (JavaScript Object Notation), qui est la norme utilisée par l'API interrogée.


