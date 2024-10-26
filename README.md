# france-inflation-data-cleaned
Données d'inflation en France à partir de 1990, nettoyées et catégorisées à partir des données INSEE, avec scripts de traitement pour faciliter l'accès et l'analyse.


# Données source

Les données brutes proviennent de l'INSEE et sont accessibles via [cette page](https://www.insee.fr/fr/statistiques/series/102342213), intitulée "Indices des prix à la consommation - Résultats par regroupement de produits et produits détaillés (COICOP)". 

Bien que ce titre puisse prêter à confusion, ces données incluent à la fois les produits de la nomenclature COICOP et ceux qui ne font pas partie de cette nomenclature. 

Cependant, l'INSEE ne fournit pas toujours les jeux de données sous une forme consolidée pour des besoins spécifiques comme ceux que j'avais (exemple : IPC pour la France entière et les produits non nomenclature sur plusieurs années), rendant leur extraction et leur traitement assez difficiles.

# Mise à jour des données

Les données disponibles dans ce dépôt sont extraites de la page de l'INSEE mentionnée ci-dessus, et correspondent à l'état des données au **15 octobre 2024**. Ce dépôt sera mis à jour à chaque nouvelle publication des données par l'INSEE.

# Traitement des données

Les jeux de données fournis dans ce dépôt résultent de mes propres besoins. Voici les étapes principales de mon traitement :

- **Colonnes supprimées** : J'ai retiré les colonnes `idBank`, `Dernière mise à jour`, et `Période`, qui pourraient intéresser certains utilisateurs mais qui n'étaient pas pertinentes pour mon cas d'usage.
- **Conversion des données** : Toutes les colonnes numériques ont été converties en valeurs numériques pour traiter les valeurs manquantes de manière cohérente.
- **Catégorisation** : J'ai ajouté plusieurs colonnes pour catégoriser les données selon le type de ménages, les départements, les types d'indices (glissement annuel, variations mensuelles, etc.) et si les produits suivent la nomenclature COICOP. J'ai également filtré les lignes où l'indice est basé sur des bases autres que l'année 2015 ou où les données sont marquées comme "série arrêtée" (par exemple, pour la région de Mayotte, toutes les données sont arrêtées et donc non incluses dans mes jeux de données).
- **Calculs** : J'ai aussi calculé les glissement annuels et variations mensuelles pour l'ensemble des ménages pour les départements suivantes : Guadeloupe, Guyane, La Réunion, Martinique, car ces données manquaient dans le jeu de données officiel.

Les jeux de données traités reflètent ainsi mes propres besoins et ne conviendront peut-être pas à tous les usages.

# Convention de nommage des fichiers

Les fichiers de données suivent une convention de nommage qui permet de comprendre les informations qu'ils contiennent. Chaque fichier est nommé sous la forme :  
`<Catégorie de ménage>_<Région>_<Type d'indice>_<Type de variation>_<Nomenclature ou NonNomenclature>.csv`

Par exemple :  
**Menages_urbains_dont_le_chef_est_ouvrier_ou_employe_France_IPC_Glissement_annuel_Nomenclature.csv** signifie :
- Le type de ménage étudié est "Ménages urbains dont le chef est ouvrier ou employé"
- Les données sont le glissement annuel de l'IPC (indice des prix à la consommation)
- Elles concernent la France entière
- Les produits étudiés sont définis par la nomenclature COICOP

Un autre exemple, **Ensemble_des_menages_Guyane_IPC_None_NonNomenclature.csv**, indiquerait :
- Le type de ménage est "Ensemble des ménages"
- La région concernée est la Guyane
- Les données correspondent à l'IPC
- Les produits ne font pas partie de la nomenclature COICOP

Cette convention de nommage permet de rapidement identifier le contenu de chaque fichier et de sélectionner les données pertinentes selon les besoins.

# Remarques importantes

- Les données pour les séries arrêtées, comme celles pour **Mayotte**, ne sont pas incluses.
- J'ai également exclu les données dont la base de calcul n'est pas l'année 2015 (comme les anciennes bases 100).
- Les glissements annuels et variations mensuelles pour l'Indice des Prix à la Consommation pour l'ensemble des ménages des départements Guadeloupe, Guyane, La Réunion, Martinique ont été manuellement calculés. 
- Mon objectif était de simplifier et de nettoyer les données pour un usage plus spécifique, en éliminant des informations que je jugeais inutiles dans mon contexte.

# Licence

Ce dépôt est distribué sous licence MIT. Les données brutes proviennent de l'INSEE, un organisme public français, et sont redistribuées ici sous forme brute et sous une forme traitée à des fins de commodité.
