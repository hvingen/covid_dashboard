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

# Plot Tab 1
def plot_covid(df, year, total_reported, hospital_admission, deceased, province, municipalities, months):
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

# Plot Tab2 en Tab3
def plot_heatmap(gdf, column, title, cmap='OrRd', legend=True, edgecolor='0.8'):
    ax = gdf.plot(
        column=column,
        cmap=cmap,
        edgecolor=edgecolor,
        figsize=(10, 8),
        linewidth=0.5,
        legend=legend,
        legend_kwds={'label': column.replace('_', ' '), 'orientation': 'vertical'},
        missing_kwds={"color": "lightgrey", "label": "No data"}
    )
    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.set_axis_off()

    # Noordpijl
    x, y, arrowlength = 0, 0, 0.2
    angle = 90
    dx = arrowlength * np.cos(np.radians(angle))
    dy = arrowlength * np.sin(np.radians(angle))

    ax.annotate('N', xy=(x, y), xytext=(x - dx, y - dy),
                arrowprops=dict(facecolor='black', width=5, headwidth=15),
                ha='center', va='center', fontsize=20,
                xycoords=ax.transAxes)

    plt.show()

def plot_province_heatmap(gdf, column):
    plot_heatmap(gdf, column=column, title="Besmetting per provincie")

def plot_municipality_heatmap(gdf, column):
    plot_heatmap(gdf, column=column, title="Besmetting per gemeente")

def plot_province_heatmap_riool(gdf, column):
    plot_heatmap(gdf, column=column, title="Rioolwater per provincie")

def plot_municipality_heatmap_riool(gdf, column):
    plot_heatmap(gdf, column=column, title="Rioolwater per gemeente")
