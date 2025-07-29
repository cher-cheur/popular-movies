# src/data_processing.py
import pandas as pd

def analyze_distributors(df_full_period: pd.DataFrame) -> pd.DataFrame:
    # ... (code de la fonction analyze_distributors)
    if df_full_period.empty:
        print("DataFrame vide fourni pour l'analyse des distributeurs.")
        return pd.DataFrame()
    df_full_period['value'] = pd.to_numeric(df_full_period['value'], errors='coerce')
    df_full_period.dropna(subset=['value'], inplace=True)
    distributor_summary = df_full_period.groupby('group')['value'].sum().sort_values(ascending=False).reset_index()
    distributor_summary.columns = ['Distributor', 'Total Gross']
    return distributor_summary

def get_unique_movies(df_full_period: pd.DataFrame) -> list:
    # ... (code de la fonction get_unique_movies)
    if df_full_period.empty:
        print("DataFrame vide fourni pour l'extraction des noms de films uniques.")
        return []
    return df_full_period['name'].unique().tolist()