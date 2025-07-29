# test_data_ingestion.py
from datetime import date
from src.data_ingestion import collect_data_for_period
from src.config import BASE_DIR # Pour sauvegarder les données

# Choisissez une petite période pour le test, ex: 3 jours en 2023
TEST_START_DATE = date(2023, 1, 1)
TEST_END_DATE = date(2023, 1, 3) # Inclut 3 jours: 1er, 2, 3

print(f"Collecting data from {TEST_START_DATE} to {TEST_END_DATE}...")
df_test_raw = collect_data_for_period(TEST_START_DATE, TEST_END_DATE)

if not df_test_raw.empty:
    print(f"Collected {len(df_test_raw)} rows of data.")
    print("First 5 rows:")
    print(df_test_raw.head())

    # Sauvegardez le résultat pour le test du prochain module
    output_path = BASE_DIR + 'raw/test_raw_data.csv'
    import os
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    df_test_raw.to_csv(output_path, index=False)
    print(f"Test data saved to {output_path}")
else:
    print("No data collected for the test period.")