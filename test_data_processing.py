# test_data_processing.py
import pandas as pd
from src.data_processing import analyze_distributors, get_unique_movies
from src.config import BASE_DIR

# Chargez les données test générées par data_ingestion.py
input_path = BASE_DIR + 'raw/test_raw_data.csv'

try:
    df_test_raw = pd.read_csv(input_path)
    df_test_raw['time'] = pd.to_datetime(df_test_raw['time']) # Convertir la colonne time
    print(f"Loaded {len(df_test_raw)} rows from {input_path}")

    # Test analyze_distributors
    distributor_summary = analyze_distributors(df_test_raw)
    print("\nDistributor Summary (first 5 rows):")
    print(distributor_summary.head())

    # Test get_unique_movies
    unique_movies = get_unique_movies(df_test_raw)
    print("\nUnique Movies (first 10):")
    print(unique_movies[:10])

    # Sauvegardez le résumé des distributeurs
    output_summary_path = BASE_DIR + 'processed/test_distributor_summary.csv'
    import os
    if not os.path.exists(os.path.dirname(output_summary_path)):
        os.makedirs(os.path.dirname(output_summary_path))
    distributor_summary.to_csv(output_summary_path, index=False)
    print(f"Distributor summary saved to {output_summary_path}")

except FileNotFoundError:
    print(f"Error: {input_path} not found. Please run test_data_ingestion.py first.")
except Exception as e:
    print(f"An error occurred during data processing test: {e}")