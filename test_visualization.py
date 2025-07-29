# test_visualization.py
from datetime import date
import pandas as pd
from src.visualization import create_chart_race_animation
from src.config import BASE_DIR, OUTPUT_DIR

# Chargez les données test (utilisez les mêmes que pour data_ingestion/processing)
input_path = BASE_DIR + 'raw/test_raw_data.csv'
TEST_START_DATE = date(2023, 1, 1)
TEST_END_DATE = date(2023, 1, 3)

try:
    df_test_raw = pd.read_csv(input_path)
    df_test_raw['time'] = pd.to_datetime(df_test_raw['time'])
    print(f"Loaded {len(df_test_raw)} rows for visualization test.")

    # Préparez les mappings nécessaires pour la visualisation
    # Copiez la logique de main.py ou de data_processing pour générer ces maps
    all_groups = df_test_raw['group'].unique()
    import random
    random.seed(42) # Pour la reproductibilité
    colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in all_groups]
    ncolors_map = dict(zip(all_groups, colors))
    groups_map = df_test_raw.set_index('name')['group'].to_dict()

    # Définissez le chemin de sortie de la vidéo test
    video_output_path = OUTPUT_DIR + 'videos/test_chart_race.mp4'

    print(f"Creating test chart race animation from {TEST_START_DATE} to {TEST_END_DATE}...")
    create_chart_race_animation(
        full_data_df=df_test_raw,
        start_date=TEST_START_DATE,
        end_date=TEST_END_DATE,
        output_path=video_output_path,
        groups_map=groups_map,
        colors_map=ncolors_map,
        fps=5 # Testez avec un FPS plus bas pour accélérer la génération du test
    )
    print(f"Test animation saved to {video_output_path}")

except FileNotFoundError:
    print(f"Error: {input_path} not found. Please run test_data_ingestion.py first.")
except Exception as e:
    print(f"An error occurred during visualization test: {e}")