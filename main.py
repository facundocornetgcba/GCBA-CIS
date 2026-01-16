from config.settings import CONFIG_HOJAS, HOJAS_GID, BASE_DIR
from extract.sheets import read_sheet
from transform.normalizacion import procesar_hoja
from load.supabase import cargar_supabase

for hoja, cfg in CONFIG_HOJAS.items():
    df = read_sheet(hoja, HOJAS_GID[hoja])
    ruta_limpio = procesar_hoja(hoja, df, cfg, BASE_DIR)

    cargar_supabase({
        "ruta_parquet": ruta_limpio,
        "tabla": "cis_registros" if hoja == "Datos" else "cis_info",
        "col_fecha": "fecha_ingreso" if hoja == "Datos" else "fecha",
        "columns_to_insert": cfg["columnas_limpio"][:-1],
        "columnas_fecha": cfg["columnas_fecha"],
        "clave_negocio": cfg["clave_negocio"]
    })

print("🏁 Pipeline finalizado")
