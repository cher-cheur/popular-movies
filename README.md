# Popular Movies - Chart Race Project

Ce projet Python génère des "chart races" (courses de graphiques) animées montrant les films les plus rentables sur une période donnée, ainsi que des analyses sur les distributeurs de films.

## Fonctionnalités

* **Scraping de données** : Récupération quotidienne des données de box-office depuis Box Office Mojo.
* **Pipeline de données structuré** : Organisation du code en modules dédiés pour l'ingestion, le traitement et la visualisation des données.
* **Stockage persistant des données** : Sauvegarde des données brutes et traitées pour une réutilisation facile et des analyses approfondies.
* **"Chart Race" dynamique** : Génération de vidéos MP4 fluides visualisant l'évolution du classement des films par leurs recettes brutes.
* **Analyse des distributeurs** : Calcul des recettes totales par distributeur et identification des acteurs majeurs du marché cinématographique.
* **Nommage intelligent des fichiers** : Les fichiers de sortie (données, vidéos, rapports) sont nommés dynamiquement en fonction de la période de données couverte.

## Technologies Utilisées

* **Python**
* **Pandas** (pour la manipulation des données)
* **Matplotlib** (pour les visualisations et animations)
* **FFmpeg** (outil externe pour la génération de vidéos)

## Comment lancer le projet

1.  **Cloner le dépôt :**
    ```bash
    git clone [URL_DE_VOTRE_DEPOT]
    cd popular-movies
    ```
2.  **Créer un environnement virtuel et installer les dépendances :**
    ```bash
    uv venv
    source .venv/bin/activate # ou `venv\Scripts\activate` sous Windows
    uv pip install -r requirements.txt
    ```
3.  **Installer FFmpeg :** Assurez-vous que FFmpeg est installé sur votre système et accessible via la ligne de commande.
    * [Instructions FFmpeg](https://ffmpeg.org/download.html)
4.  **Configurer les dates (optionnel) :** Modifiez `src/config.py` pour ajuster les dates de début et de fin de la collecte de données.
5.  **Exécuter le pipeline :**
    ```bash
    python src/main.py
    ```
    Les données seront collectées (ou chargées si déjà existantes), traitées, et la vidéo de la "chart race" ainsi que les analyses seront générées dans le répertoire `output/`.

## Structure du Projet

````
popular-movies/
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   ├── config.py             # Configurations globales
│   ├── data_ingestion.py     # Récupération des données depuis Box Office Mojo
│   ├── data_processing.py    # Nettoyage, transformation et analyse des données
│   ├── visualization.py      # Création des graphiques et animations
│   ├── utils.py              # Fonctions utilitaires génériques (ex: nommage de fichiers)
│   └── main.py               # Orchestre le pipeline complet du projet
├── data/
│   ├── raw/                  # Données brutes scrapées
│   └── processed/            # Données agrégées et traitées
└── output/
├── videos/               # Vidéos de chart race générées
├── images/               # Graphiques statiques générés (si applicable)
└── descriptions/         # Fichiers de résumé et de description

````