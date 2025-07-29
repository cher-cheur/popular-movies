# src/visualization.py

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import pandas as pd
from datetime import date, timedelta
import os

def draw_barchart(day: date, data_for_day: pd.DataFrame, all_groups_map: dict, colors_map: dict, ax: plt.Axes, year: int):
    """
    Dessine un seul graphique à barres horizontal pour un jour donné.

    Args:
        day (date): La date du jour à dessiner.
        data_for_day (pd.DataFrame): DataFrame contenant les données des films pour le jour spécifié.
                                      Doit contenir les colonnes 'name', 'value', 'group'.
        all_groups_map (dict): Un dictionnaire mappant les noms de films à leurs groupes (distributeurs).
        colors_map (dict): Un dictionnaire mappant les noms de groupe (distributeurs) à leurs couleurs.
        ax (plt.Axes): L'objet Axes de Matplotlib sur lequel dessiner.
        year (int): L'année principale du projet, utilisée pour le titre.
    """
    ax.clear()

    # --- DÉBUT DE LA CORRECTION DU SettingWithCopyWarning ---
    # Traitez une copie explicite pour éviter le SettingWithCopyWarning
    df_plot = data_for_day.copy()
    df_plot.loc[:, 'value'] = pd.to_numeric(df_plot['value'], errors='coerce')
    df_plot.dropna(subset=['value'], inplace=True)

    # Sélectionne les 10 films les plus rentables pour le jour donné
    dff = df_plot.sort_values(by='value', ascending=True).tail(10)
    # --- FIN DE LA CORRECTION DU SettingWithCopyWarning ---

    # Dessine les barres
    bar_colors = [colors_map.get(x, '#808080') for x in dff['group']]
    ax.barh(dff['name'], dff['value'], color=bar_colors, alpha=0.75)

    # Ajoute le texte (noms des films, groupes, valeurs)
    dx = dff['value'].max() / 200
    for i, (value, name) in enumerate(zip(dff['value'], dff['name'])):
        group_name = all_groups_map.get(name, 'N/A')
        ax.text(value - dx, i, name, color='#DFDFDF', size=14, weight=600, ha='right', va='bottom')
        ax.text(value - dx, i - 0.25, group_name, size=10, color='#DFDFDF', ha='right', va='baseline')
        ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')

    # Ajoute la date actuelle
    ax.text(1, 0.1, str(day.strftime('%Y-%m-%d')), transform=ax.transAxes, color='#DFDFDF', size=35, ha='right', weight=800)

    # Ajoute les titres et labels
    ax.text(0, 1.06, 'Total Gross in $', transform=ax.transAxes, color='#DFDFDF', size=12)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#B5B5B5', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.15, f'Highest grossing movies of {year}',
            transform=ax.transAxes, color='#DFDFDF', size=24, weight=600, ha='left', va='top')
    ax.text(1, 0, 'by @dataera; credits @pratapvardhan @jburnmurdoch', transform=ax.transAxes, color='#DFDFDF', ha='right',
            bbox=dict(facecolor='#3A3A3A', alpha=0.4, edgecolor='white'))
    plt.box(False)
    plt.tight_layout()
def create_chart_race_animation(
    full_data_df: pd.DataFrame,
    start_date: date,
    end_date: date,
    output_path: str,
    groups_map: dict,
    colors_map: dict,
    fps: int = 24, # Augmenté pour une meilleure fluidité
    bitrate: int = 1800
):
    """
    Crée et sauvegarde l'animation de la chart race.

    Args:
        full_data_df (pd.DataFrame): DataFrame contenant toutes les données de films pour la période.
                                     Doit avoir les colonnes 'name', 'value', 'group', 'time'.
        start_date (date): Date de début de la période pour l'animation.
        end_date (date): Date de fin de la période pour l'animation.
        output_path (str): Chemin complet où sauvegarder la vidéo de l'animation.
        groups_map (dict): Dictionnaire mappant les noms de films à leurs groupes (distributeurs).
        colors_map (dict): Dictionnaire mappant les noms de groupe (distributeurs) à leurs couleurs.
        fps (int): Cadres par seconde pour l'animation (fluidité).
        bitrate (int): Bitrate de la vidéo en kbps.
    """
    if full_data_df.empty:
        print("Le DataFrame de données est vide. Impossible de créer l'animation.")
        return

    # Assurez-vous que 'time' est au format datetime
    full_data_df['time'] = pd.to_datetime(full_data_df['time'])
    
    # Déterminez l'année pour le titre du graphique (peut être la première année de la période)
    # Ou vous pouvez rendre cela plus dynamique si l'animation couvre plusieurs années
    display_year = start_date.year 

    fig, ax = plt.subplots(figsize=(15, 8), facecolor='#3A3A3A') # Définir la couleur de fond ici
    plt.rcParams['text.color'] = '#DFDFDF' # Couleur de texte par défaut pour Matplotlib

    # Générer la séquence de jours pour les frames
    # Pour une transition plus fluide (interpolation), cette partie devrait être plus complexe,
    # générant des frames intermédiaires. Pour l'instant, c'est un frame par jour de données.
    
    # Filtrer les données pour la période spécifiée
    df_filtered = full_data_df[(full_data_df['time'] >= pd.to_datetime(start_date)) &
                               (full_data_df['time'] <= pd.to_datetime(end_date))]
    
    # Obtenir la liste des jours uniques dans les données filtrées
    unique_days = df_filtered['time'].dt.normalize().unique()
    unique_days_list = sorted([pd.to_datetime(d).date() for d in unique_days])

    # S'il n'y a pas de données pour la période, ne pas créer d'animation
    if not unique_days_list:
        print(f"Aucune donnée disponible entre {start_date} et {end_date} pour l'animation.")
        plt.close(fig) # Ferme la figure vide
        return

    def update(day_idx):
        current_day = unique_days_list[day_idx]
        data_for_current_day = df_filtered[df_filtered['time'] == pd.to_datetime(current_day)]
        draw_barchart(current_day, data_for_current_day, groups_map, colors_map, ax, display_year)

    # Le nombre de frames correspond au nombre de jours uniques dans la période
    num_frames = len(unique_days_list)

    animator = animation.FuncAnimation(
        fig,
        update,
        frames=num_frames, # Nombre de jours uniques pour les frames
        interval=1000/fps, # Délai entre les frames en ms
        repeat=False,
        blit=False # Souvent défini sur False pour les animations complexes
    )

    # Assurez-vous que le répertoire de sortie existe
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Sauvegarde de l'animation dans {output_path}...")
    animator.save(output_path, fps=fps, bitrate=bitrate, savefig_kwargs={'facecolor': '#3A3A3A'})
    print("Animation sauvegardée avec succès.")
    plt.close(fig) # Ferme la figure pour libérer de la mémoire