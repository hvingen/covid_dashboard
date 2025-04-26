import os
from config import EXPORTS_DIR
from datetime import datetime
import pandas as pd

EXPORTS_DIR = os.path.join(os.getcwd(), "/notebooks/exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)

def export_dataframe(df, format="csv", name="export", full=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "full" if full else "small"
    filename = f"{name}_{suffix}_{timestamp}.{format}"
    filepath = os.path.join(EXPORTS_DIR, filename)

    if format == "csv":
        df.to_csv(filepath, index=False)
    elif format == "md":
        with open(filepath, "w") as f:
            f.write(f"# Samenvatting: {name}\n\n")
            f.write(df.to_markdown(index=False))
    elif format == "pdf":
        # Markdown naar HTML naar PDF (vereist nbconvert of weasyprint)
        import markdown
        from weasyprint import HTML

        html = markdown.markdown(df.to_markdown(index=False))
        HTML(string=html).write_pdf(filepath)
    else:
        raise ValueError("Unsupported export format")

    return filepath

import ipywidgets as widgets
from IPython.display import display
from export_utils import export_dataframe

def create_export_widget(data_small, data_full, label):
    dropdown = widgets.Dropdown(
        options=[
            ('Export small CSV', 'csv_small'),
            ('Export full CSV', 'csv_full'),
            ('Export to Markdown', 'md'),
            ('Export to PDF', 'pdf')
        ],
        description='Export:',
        layout=widgets.Layout(width='250px')
    )

    def handle_export(change):
        if change['type'] == 'change' and change['name'] == 'value':
            choice = change['new']
            if choice == 'csv_small':
                export_dataframe(data_small, format='csv', name=label, full=False)
            elif choice == 'csv_full':
                export_dataframe(data_full, format='csv', name=label, full=True)
            elif choice == 'md':
                export_dataframe(data_small, format='md', name=label)
            elif choice == 'pdf':
                export_dataframe(data_small, format='pdf', name=label)
            dropdown.value = None  # reset na actie

    dropdown.observe(handle_export)
    return dropdown
