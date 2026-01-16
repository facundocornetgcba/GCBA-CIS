import pandas as pd
from config.settings import SHEET_ID

def read_sheet(nombre_hoja, gid):
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv&gid={gid}"
    )
    df = pd.read_csv(url)
    print(f"📥 {nombre_hoja}: {len(df)} registros leídos")
    return df
