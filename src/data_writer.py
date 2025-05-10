from config import CSV_DIR
import pandas as pd
import os

def Saveframes(verbose=True):
    """
    Download COVID-19 datasets van RIVM en sla ze op in /data/csv.

    Returns:
        dict: Mapping van bestandsnaam → status (geslaagd of fout).
    """
    urls = {
        'COVID-19_aantallen_gemeente_per_dag.csv':
            'https://data.rivm.nl/data/covid-19/COVID-19_aantallen_gemeente_per_dag.csv',
        'COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv':
            'https://data.rivm.nl/data/covid-19/COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv',
        'COVID-19_ziekenhuisopnames.csv':
            'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames.csv',
        'COVID-19_ziekenhuisopnames_tm_03102021.csv':
            'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames_tm_03102021.csv',
        'COVID-19_rioolwaterdata.csv':
            'https://data.rivm.nl/data/covid-19/COVID-19_rioolwaterdata.csv'
    }

    os.makedirs(CSV_DIR, exist_ok=True)

    results = {}
    for fname, url in urls.items():
        try:
            df = pd.read_csv(url, sep=';')
            df.to_csv(CSV_DIR / fname, sep=';', index=False)
            results[fname] = '✅ Geslaagd'
            if verbose:
                print(f"✅ {fname} opgeslagen.")
        except Exception as e:
            results[fname] = f"❌ Fout: {str(e)}"
            if verbose:
                print(f"❌ Mislukt voor {fname}: {e}")

    return results