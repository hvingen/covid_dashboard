import sys
from pathlib import Path

# Dynamisch projectpad instellen zodat config gevonden wordt
project_root = Path(__file__).resolve()
while not (project_root / "config.py").exists() and project_root != project_root.parent:
    project_root = project_root.parent

sys.path.insert(0, str(project_root))

from config import SHAPEFILES_DIR
import matplotlib.pyplot as plt
import numpy as np

def plot_covid(
    df,
    year,
    total_reported=True,
    hospital_admission=True,
    deceased=True,
    province='Netherlands',
    municipalities=False,
    months=False,
    save_as=None,
    dpi=300
):
    """
    Plot COVID-19 gerelateerde statistieken als staafdiagram.

    Parameters:
    - df (DataFrame): Dataset met Covid-informatie.
    - year (int): Te selecteren jaar.
    - total_reported (bool): Toon aantal meldingen.
    - hospital_admission (bool): Toon ziekenhuisopnames.
    - deceased (bool): Toon overledenen.
    - province (str): Provincie ('Netherlands', 'All provinces' of specifieke naam).
    - municipalities (bool): Toon op gemeentelijk niveau (alleen bij specifieke provincie).
    - months (bool): Groepeer op maand (alleen bij Netherlands of provincie).
    - save_as (str or None): Bestandsnaam om op te slaan ('.png' of '.pdf'), of None voor alleen weergave.
    - dpi (int): Resolutie van de uitvoer (default: 300).

    Returns:
    - matplotlib.figure.Figure: De gegenereerde figuur (voor verdere verwerking of tests).
    """
    filtered_df = df[df['Year'] == year]

    # Aggregatie op basis van selectie
    if province == 'Netherlands':
        if months:
            grouped_df = (
                filtered_df.groupby(['Month', 'Month_name'])[['Total_reported', 'Hospital_admission', 'Deceased']]
                .sum()
                .sort_values(by='Month')
            )
            grouped_df.reset_index(level=0, drop=True, inplace=True)
        else:
            grouped_df = filtered_df.groupby('Year')[['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif province == 'All provinces':
        grouped_df = filtered_df.groupby('Province_merged')[['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif municipalities:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = filtered_df.groupby('Municipality_name_merged')[['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif months:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = (
            filtered_df.groupby(['Month', 'Month_name'])[['Total_reported', 'Hospital_admission', 'Deceased']]
            .sum()
        )
        grouped_df.reset_index(level=0, drop=True, inplace=True)
    else:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = filtered_df.groupby('Province_merged')[['Total_reported', 'Hospital_admission', 'Deceased']].sum()

    # Plotvoorbereiding
    x_labels = grouped_df.index
    x = np.arange(len(x_labels)) if len(x_labels) > 1 else np.array([0])
    bar_width = 0.25

    # Dynamische figuurbreedte
    n = len(x)
    if n < 10:
        figsize = (15, 6)
    elif n < 15:
        figsize = (20, 6)
    elif n < 20:
        figsize = (24, 7)
    elif n < 25:
        figsize = (24, 9)
    elif n < 30:
        figsize = (26, 9)
    else:
        figsize = (28, 10)

    fig, ax = plt.subplots(figsize=figsize)

    if total_reported:
        ax.bar(x - bar_width, grouped_df['Total_reported'], width=bar_width, color='steelblue', label='Reported')
    if hospital_admission:
        ax.bar(x, grouped_df['Hospital_admission'], width=bar_width, color='seagreen', label='Hospital')
    if deceased:
        ax.bar(x + bar_width, grouped_df['Deceased'], width=bar_width, color='darkorange', label='Deceased')

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=45)
    if int(year) >= 2023:
        ax.set_xlabel('⚠️ Not all RIVM data is available after 1-1-2023', color='red', fontsize=10)
    else:
        ax.set_xlabel('Time period')
    ax.set_ylabel('Number')
    ax.set_title(f'COVID-19 data for {year} ({province})', fontsize=14, fontweight='bold')
    ax.ticklabel_format(style='plain', axis='y')
    if any([total_reported, hospital_admission, deceased]):
        ax.legend()
    fig.tight_layout()

    if save_as:
        plt.savefig(save_as, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig

def plot_heatmap(
    gdf,
    column,
    title,
    cmap='OrRd',
    legend=True,
    edgecolor='0.8',
    figsize=(8, 6),
    dpi=300,
    save_as=None,
    arrow_position='bottomright'
):
    """
    Plot een heatmap met optionele noordpijl en opslagoptie.

    Parameters:
    - gdf (GeoDataFrame): De geodata.
    - column (str): De kolom waarop de kleur gebaseerd wordt.
    - title (str): De titel van de kaart.
    - cmap (str): Kleurenkaart (default: 'OrRd').
    - legend (bool): Toon legenda (default: True).
    - edgecolor (str): Randkleur polygons (default: '0.8').
    - figsize (tuple): Grootte van de figuur (default: (10, 8)).
    - dpi (int): Resolutie voor opslag (default: 300).
    - save_as (str or None): Bestandsnaam om op te slaan (bv. 'kaart.png') of None om alleen te tonen.
    - arrow_position (str): Locatie van noordpijl ('topleft', 'topright', 'bottomleft', 'bottomright').

    Returns:
    - matplotlib.axes.Axes: De gegenereerde plot.
    """
    fig, ax = plt.subplots(figsize=figsize)
    gdf.plot(
        column=column,
        cmap=cmap,
        edgecolor=edgecolor,
        linewidth=0.5,
        legend=legend,
        legend_kwds={'label': column.replace('_', ' '), 'orientation': 'vertical'},
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax
    )

    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.set_axis_off()

    # Noordpijl
    pos_dict = {
        'topleft': (0.1, 0.9),
        'topright': (0.9, 0.9),
        'bottomleft': (0.1, 0.1),
        'bottomright': (0.9, 0.1)
    }
    x, y = pos_dict.get(arrow_position, (0.9, 0.1))
    arrowlength = 0.08
    angle = 90
    dx = arrowlength * np.cos(np.radians(angle))
    dy = arrowlength * np.sin(np.radians(angle))

    ax.annotate('N', xy=(x, y), xytext=(x - dx, y - dy),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=16,
                xycoords=ax.transAxes)

    if save_as:
        plt.savefig(save_as, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return ax

def plot_province_heatmap(gdf, column):
    plot_heatmap(gdf, column=column, title="Besmetting per provincie")

def plot_municipality_heatmap(gdf, column):
    plot_heatmap(gdf, column=column, title="Besmetting per gemeente")

def plot_province_heatmap_riool(gdf, column):
    plot_heatmap(gdf, column=column, title="Rioolwater per provincie")

def plot_municipality_heatmap_riool(gdf, column):
    plot_heatmap(gdf, column=column, title="Rioolwater per gemeente")
