# src/main.py

from datetime import date
import os
import pandas as pd

# Importez les configurations
from config import START_DATE, END_DATE, BASE_DIR, OUTPUT_DIR, TODROP_COLUMNS

# Importez les fonctions des modules dédiés
from data_ingestion import collect_data_for_period
from data_processing import analyze_distributors, get_unique_movies
from visualization import create_chart_race_animation

# Importez les fonctions utilitaires
from utils import generate_file_date_suffix, create_directory_if_not_exists

def run_project():
    """Exécute l'ensemble du pipeline du projet."""

    # Générer le suffixe de date une seule fois
    date_suffix = generate_file_date_suffix(START_DATE, END_DATE)

    # 1. Création des répertoires nécessaires
    print("Vérification et création des répertoires de projet...")
    create_directory_if_not_exists(os.path.join(BASE_DIR, 'raw'))
    create_directory_if_not_exists(os.path.join(BASE_DIR, 'processed'))
    create_directory_if_not_exists(os.path.join(OUTPUT_DIR, 'videos'))
    create_directory_if_not_exists(os.path.join(OUTPUT_DIR, 'images'))
    create_directory_if_not_exists(os.path.join(OUTPUT_DIR, 'descriptions'))
    print("Répertoires prêts.")

    # 2. Collecte ou chargement des données brutes
    raw_data_filename = f"box_office_daily_{date_suffix}.csv"
    raw_data_path = os.path.join(BASE_DIR, 'raw', raw_data_filename)
    df_full_period = pd.DataFrame()

    if os.path.exists(raw_data_path):
        print(f"Chargement des données existantes depuis {raw_data_path}...")
        try:
            df_full_period = pd.read_csv(raw_data_path)
            df_full_period['time'] = pd.to_datetime(df_full_period['time'])
            print("Données chargées avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}. Tentative de re-collecte.")
            df_full_period = collect_data_for_period(START_DATE, END_DATE)
            if not df_full_period.empty:
                df_full_period.to_csv(raw_data_path, index=False)
                print(f"Nouvelles données collectées et sauvegardées dans {raw_data_path}")
            else:
                print("Aucune donnée collectée après la tentative de re-collecte.")
    else:
        print("Aucun fichier de données brutes trouvé. Collecte des nouvelles données...")
        df_full_period = collect_data_for_period(START_DATE, END_DATE)
        if not df_full_period.empty:
            df_full_period.to_csv(raw_data_path, index=False)
            print(f"Données collectées et sauvegardées dans {raw_data_path}")
        else:
            print("Aucune donnée collectée.")


    if df_full_period.empty:
        print("Aucune donnée collectée ou chargée. Le processus s'arrête.")
        return

    # 3. Analyse des distributeurs
    print("Début de l'analyse des distributeurs...")
    distributor_summary = analyze_distributors(df_full_period)
    processed_distributor_filename = f"distributor_summary_{date_suffix}.csv"
    processed_distributor_path = os.path.join(BASE_DIR, 'processed', processed_distributor_filename)
    distributor_summary.to_csv(processed_distributor_path)
    print(f"Résumé des distributeurs sauvegardé dans {processed_distributor_path}.")

    # 4. Préparation des mappings pour la visualisation
    all_groups = df_full_period['group'].unique()
    import random
    random.seed(42)
    colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in all_groups]
    ncolors_map = dict(zip(all_groups, colors))
    groups_map = df_full_period.set_index('name')['group'].to_dict()

    # 5. Création de la Chart Race
    print("Génération de la chart race...")
    chart_race_video_filename = f"chart_race_{date_suffix}.mp4"
    chart_race_output_path = os.path.join(OUTPUT_DIR, 'videos', chart_race_video_filename)
    create_chart_race_animation(
        full_data_df=df_full_period,
        start_date=START_DATE,
        end_date=END_DATE,
        output_path=chart_race_output_path,
        groups_map=groups_map,
        colors_map=ncolors_map
    )
    print(f"Chart race sauvegardée dans {chart_race_output_path}")

    # 6. Génération de la description du projet
    highest_grossing_movie = df_full_period.loc[df_full_period['value'].idxmax()]
    description_filename = f"project_summary_{date_suffix}.txt"
    desc_file_path = os.path.join(OUTPUT_DIR, 'descriptions', description_filename)

    with open(desc_file_path, "w+") as f:
        f.write(f"In this dataset, we handled {len(df_full_period)} movie observations between {START_DATE} and {END_DATE}.\n")
        f.write(f"What film had the biggest box office gross in this period? \n")
        f.write(f"{highest_grossing_movie['name']} distributed by {highest_grossing_movie['group']} had made ${highest_grossing_movie['value']:,}.\n")
        f.write("Here is the list of movie names you will see in this video:\n")
        f.write(str(get_unique_movies(df_full_period)))
    print(f"Description du projet sauvegardée dans {desc_file_path}.")

    print("Pipeline du projet terminé avec succès!")

if __name__ == "__main__":
    run_project()