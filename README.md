Ce programme sert à trouver les séances programmées à la Cinémathèque pour le trimestre actuel, et permet également de filtrer ces séances par date. Elles sont ensuite enregistrées dans un fichier au format standard CSV, et peuvent donc être consultées dans un tableur.

Il est possible de fournir des arguments dans une console lors de l'exécution afin de modifier les résultats obtenus:

    -> date_filter: Demande de n'afficher que les séances qui ont lieu à un jour précis. La date fournie doit être sous la forme annee-numero_mois-numero_jour. Par exemple, pour afficher les séances du 11 juillet 2024, il faut saisir date_filter=2024-07-11. Si aucune date n'est spécifiée, alors le programme filtre les séances par la date actuelle.

    -> filter: Filtre les films selon un contenu spécifié. Par exemple, pour afficher uniquement les films de James Cameron, il faut saisir filter=James Cameron.

    


