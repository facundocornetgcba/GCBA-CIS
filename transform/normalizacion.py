import pandas as pd
import re
import os

def normalize_dni(val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    val = re.sub(r"\.0$", "", val)
    return val.replace(".", "").replace(",", "")

def safe_title(series):
    return series.where(
        ~series.notna(),
        series.astype(str).str.title().str.strip()
    )

def procesar_hoja(nombre, df_new, cfg, base_dir):
    # Normalizar nombres de columnas: minúsculas y sin espacios extra
    df_new.columns = df_new.columns.str.lower().str.strip()
    
    df_new["fecha_carga"] = pd.Timestamp.now()

    for col in cfg["columnas_fecha"]:
        if col in df_new.columns:
            df_new[col] = pd.to_datetime(df_new[col], errors="coerce")

    for col in df_new.select_dtypes(include="object").columns:
        df_new[col] = df_new[col].astype(str).str.strip()

    dir_hist = f"{base_dir}/historico/{nombre}"
    dir_limpio = f"{base_dir}/limpio/{nombre}"
    os.makedirs(dir_hist, exist_ok=True)
    os.makedirs(dir_limpio, exist_ok=True)

    ruta_hist = f"{dir_hist}/historico.parquet"

    if os.path.exists(ruta_hist):
        df_hist = pd.read_parquet(ruta_hist)
    else:
        df_hist = pd.DataFrame(columns=df_new.columns)

    df_total = (
        pd.concat([df_hist, df_new], ignore_index=True)
          .drop_duplicates(subset=cfg["clave_negocio"], keep="last")
    )

    df_total.to_parquet(ruta_hist, index=False)

    df_limpio = df_total[cfg["columnas_limpio"]].copy()

    if "nro_documento" in df_limpio.columns:
        df_limpio["nro_documento"] = df_limpio["nro_documento"].apply(normalize_dni)

    for col in df_limpio.select_dtypes(include="object").columns:
        df_limpio[col] = safe_title(df_limpio[col])

    ruta_limpio = f"{dir_limpio}/limpio.parquet"
    df_limpio.to_parquet(ruta_limpio, index=False)

    return ruta_limpio
