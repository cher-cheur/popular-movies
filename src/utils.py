# src/utils.py

from datetime import date
import os

def generate_file_date_suffix(start_date: date, end_date: date) -> str:
    """
    Génère un suffixe de nom de fichier basé sur les dates de début et de fin.
    Ex: '2000-12-01_to_2000-12-10'
    """
    return f"{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}"

def create_directory_if_not_exists(path: str):
    """
    Crée un répertoire s'il n'existe pas.

    Args:
        path (str): Le chemin du répertoire à créer.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Répertoire créé : {path}")