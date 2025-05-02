#%matplotlib inline
"""
TODO: Add module-level description here.
"""
from config import SHAPEFILES_DIR
import matplotlib.pyplot as plt
import pandas as pd_riool
import geopandas as gpd
from pathlib import Path
import ipywidgets as widgets
import seaborn as sns
import numpy as np

def update_heatmap_riool(year):
    from pathlib import Path
    import pandas as pd
    from data_loader import load_province_shapefile

    csv_directory = Path(__file__).resolve().parent.parent / 'data' / 'csv'
    file5 = csv_directory / 'COVID-19_rioolwaterdata.csv'

    df_inkomen = pd.read_csv(file5, sep=';')

    gdf_prov = load_province_shapefile()

    # Gebruik gemiddelde RNA-waarde als tijdelijke placeholder
    mean_rna = df_inkomen['RNA_flow_per_100000'].mean()
    gdf_prov['RNA_flow_per_100000'] = mean_rna
    columns = 'RNA_flow_per_100000'

    ax = gdf_prov.plot(
        column=columns,
        legend=True,
        figsize=(10, 8),
        edgecolor='black'
    )
    ax.set_title(f'Gemiddelde RNA/100.000 in rioolwater ({year})')
    ax.axis('off')
    columns = 'RNA_flow_per_100000'
    column = columns,
    cmap = 'OrRd',
    legend = True,
    edgecolor = 'black'
    ax.set_title("Corona besmetting in rioolwater", fontsize=15, fontweight='bold')
    ax.set_axis_off()

    # arrow
    x, y, arrowlenght = 0, 0, 0.2
    angle = 90
    dx = arrowlenght * np.cos(np.radians(angle))
    dy = arrowlenght * np.sin(np.radians(angle))

    ax.annotate('N', xy=(x, y), xytext=(x - dx, y - dy),
                  arrowprops=dict(facecolor='black', width=5, headwidth=15),
                  ha='center', va='center', fontsize=20,
                  xycoords=ax.transAxes)

    plt.show()

def update_plot(df, year, total_reported, hospital_admission, deceased, province, municipalities, months):
    """
    TODO: Describe what this function does.
    """
    """
    Generates a grouped bar chart with Covid-data upon GUI input.
    """
    # Filter by year
    filtered_df = df[df['Year'] == year]

    # Aggregation based upon input
    if province == 'Netherlands':
        if months:
            grouped_df = filtered_df.groupby(['Month', 'Month_name'])[
                ['Total_reported', 'Hospital_admission', 'Deceased']].sum().sort_values(by='Month')
            grouped_df.reset_index(level=0, drop=True, inplace=True)
        else:
            grouped_df = filtered_df.groupby('Year')[['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif province == 'All provinces':
        grouped_df = filtered_df.groupby(['Province_merged'])[
            ['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif municipalities:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = filtered_df.groupby(['Municipality_name_merged'])[
            ['Total_reported', 'Hospital_admission', 'Deceased']].sum()
    elif months:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = filtered_df.groupby(['Month', 'Month_name'])[
            ['Total_reported', 'Hospital_admission', 'Deceased']].sum()
        grouped_df.reset_index(level=0, drop=True, inplace=True)
    else:
        filtered_df = filtered_df[filtered_df['Province_merged'] == province]
        grouped_df = filtered_df.groupby(['Province_merged'])[
            ['Total_reported', 'Hospital_admission', 'Deceased']].sum()

    # Get label x values
    x_labels = grouped_df.index

    # Get bar y values
    y_total_reported = grouped_df['Total_reported'] if total_reported else None
    y_hospital_admission = grouped_df['Hospital_admission'] if hospital_admission else None
    y_deceased = grouped_df['Deceased'] if deceased else None

    # Set minimal width of bars
    x = np.arange(len(x_labels)) if len(x_labels) > 1 else np.array([0])
    bar_width = 0.25

    # Dynamic bar formatting
    if len(x) < 10:
        plt.figure(figsize=(15, 6))
    elif len(x) < 15:
        plt.figure(figsize=(20, 6))
    elif len(x) < 20:
        plt.figure(figsize=(24, 7))
    elif len(x) < 25:
        plt.figure(figsize=(24, 9))
    elif len(x) < 30:
        plt.figure(figsize=(26, 9))
    else:
        plt.figure(figsize=(28, 10))

    # Plot bars next to each other
    if y_total_reported is not None:
        plt.bar(x - bar_width, y_total_reported, width=bar_width, color='blue', label='Covid reported')
    if y_hospital_admission is not None:
        plt.bar(x, y_hospital_admission, width=bar_width, color='green', label='Hospital admission')
    if y_deceased is not None:
        plt.bar(x + bar_width, y_deceased, width=bar_width, color='orange', label='Deceased')

    # Axis-labels, title, legend
    plt.xticks(x, x_labels, rotation=45)
    if int(year) >= 2023:
        plt.xlabel('Warning: Not all RIVM data is available after 1-1-2023', color='red')
    plt.ylabel('Number')
    plt.title(f'Covid data for {year} ({province})')
    plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
    if any([total_reported, hospital_admission, deceased]):
        plt.legend()
    plt.tight_layout()
    plt.show()

def plot_province_heatmap(gdf, column='Total_reported'):
    """
    TODO: Describe what this function does.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)

    xlim = gdf.total_bounds[[0, 2]]
    ylim = gdf.total_bounds[[1, 3]]

    gdf.plot(
        column=column,
        cmap='OrRd',
        linewidth=0.5,
        ax=ax,
        edgecolor='0.8',
        legend=True,
        legend_kwds={'label': column.replace('_', ' '), 'orientation': 'vertical'},
        missing_kwds={"color": "lightgrey", "label": "No data"}
    )
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    for spine in ax.spines.values():
        spine.set_visible(False)

    leg = ax.get_legend()
    if leg:
        leg.set_bbox_to_anchor((1.02, 1))
        leg.set_title(column)

    plt.subplots_adjust(left=0.01, right=0.85)
    plt.tight_layout()
    plt.show()

def plot_province_heatmap_riool(gdf, column='RNA_flow_per_100000'):
    """
    TODO: Describe what this function does.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)

    xlim = gdf.total_bounds[[0, 2]]
    ylim = gdf.total_bounds[[1, 3]]

    gdf.plot(
        column=column,
        cmap='OrRd',
        linewidth=0.5,
        ax=ax,
        edgecolor='0.8',
        legend=True,
        legend_kwds={'label': column.replace('_', ' '), 'orientation': 'vertical'},
        missing_kwds={"color": "lightgrey", "label": "No data"}
    )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    for spine in ax.spines.values():
        spine.set_visible(False)

    leg = ax.get_legend()
    if leg:
        leg.set_bbox_to_anchor((1.02, 1))
        leg.set_title(column)

    plt.subplots_adjust(left=0.01, right=0.85)
    plt.tight_layout()
    plt.show()

def plot_municipality_heatmap_riool(gdf, column='RNA_flow_per_100000'):
    """
    TODO: Describe what this function does.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)

    xlim = gdf.total_bounds[[0, 2]]
    ylim = gdf.total_bounds[[1, 3]]

    gdf.plot(
        column=column,
        cmap='OrRd',
        linewidth=0.5,
        ax=ax,
        edgecolor='0.8',
        legend=True,
        legend_kwds={'label': column.replace('_', ' '), 'orientation': 'vertical'},
        missing_kwds={"color": "lightgrey", "label": "No data"}
    )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    for spine in ax.spines.values():
        spine.set_visible(False)

    leg = ax.get_legend()
    if leg:
        leg.set_bbox_to_anchor((1.02, 1))
        leg.set_title(column)

    plt.subplots_adjust(left=0.01, right=0.85)
    plt.tight_layout()
    plt.show()




