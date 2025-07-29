# src/data_ingestion.py
import pandas as pd
import numpy as np
from datetime import timedelta
from config import TODROP_COLUMNS # Assurez-vous d'importer TODROP_COLUMNS

def fetch_daily_data(day):
    # ... (code de la fonction fetch_daily_data)
    url = 'https://www.boxofficemojo.com/date/' + day.strftime('%Y-%m-%d') + '/'
    try:
        df = pd.read_html(url, na_values=["-"], header=0)[0]
        df.drop(columns=TODROP_COLUMNS, axis=1, inplace=True)
        df.dropna(axis=0, inplace=True)
        df['time'] = np.repeat(day.strftime("%Y-%m-%d"), len(df))
        df.columns = ['name', 'value', 'group', 'time']
        df['value'] = df.value.apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)
        return df
    except Exception as e:
        print(f"Error fetching data for {day.strftime('%Y-%m-%d')}: {e}")
        return pd.DataFrame()

def collect_data_for_period(start_date, end_date):
    # ... (code de la fonction collect_data_for_period)
    all_data = pd.DataFrame()
    current_date = start_date
    while current_date <= end_date:
        print(f"Collecting data for {current_date.strftime('%Y-%m-%d')}...")
        daily_df = fetch_daily_data(current_date)
        all_data = pd.concat([all_data, daily_df], ignore_index=True)
        current_date += timedelta(days=1)
    return all_data