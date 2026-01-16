import os
import pandas as pd
from supabase import create_client, Client
import time

SUPABASE_URL="https://awdddoqejncrheuazyvs.supabase.co"
SUPABASE_KEY="sb_secret_Nq2AyPNz4tN0-i3UU8jtYg_1R7nRlHQ"
def cargar_supabase(cfg):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en variables de entorno")

    supabase: Client = create_client(url, key)
    
    tabla = cfg["tabla"]
    col_fecha = cfg["col_fecha"]
    ruta_parquet = cfg["ruta_parquet"]
    
    print(f"🚀 Iniciando carga a tabla '{tabla}'...")
    
    df = pd.read_parquet(ruta_parquet)
    print(f"   📦 Registros en parquet: {len(df)}")
    
    # 1. Obtener última fecha para carga incremental
    try:
        response = supabase.table(tabla)\
            .select(col_fecha)\
            .order(col_fecha, desc=True)\
            .limit(1)\
            .execute()
            
        ultima_fecha = None
        if response.data and len(response.data) > 0:
            val_db = response.data[0][col_fecha]
            # Convertir string DB a objeto date puro
            if val_db:
                ultima_fecha = pd.to_datetime(val_db).date()
                print(f"   📅 Última fecha en DB: {ultima_fecha}")
        else:
            print("   📅 Tabla vacía, carga total...")

    except Exception as e:
        print(f"   ⚠️ Error consultando última fecha: {e}")
    
    # 2. Conversión y Filtrado (Logica del usuario)
    # Convertir columna fecha a datetime.date (sin hora)
    if col_fecha in df.columns:
        df[col_fecha] = pd.to_datetime(df[col_fecha], errors='coerce').dt.date

    # Manejar otras columnas de fecha para que sean strings ISO (JSON friendly) o None
    # Identificamos columnas fecha extra
    cols_fecha_extra = cfg.get("columnas_fecha", [])
    for col in cols_fecha_extra:
        if col in df.columns and col != col_fecha:
             # Convertir a date object si es posible, luego a string para subida
             df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

    # Filtrar
    if ultima_fecha is not None:
        # Comparación de objetos date vs date
        df = df[df[col_fecha] > ultima_fecha]
    
    if df.empty:
        print("   ✅ No hay registros nuevos para cargar (Filtrado por fecha)")
        return

    print(f"   📊 Registros nuevos a subir: {len(df)}")

    # 3. Preparar subida
    columnas = cfg["columns_to_insert"]
    
    # IMPORTANTE: Supabase/JSON no acepta objetos `date` de python directamente a veces
    # Lo mejor es convertir todo date a string ISO YYYY-MM-DD antes de subir
    # Iteramos sobre columnas que son tipo date/object y aseguramos string
    # Específicamente la col_fecha y las extras
    
    all_date_cols = cols_fecha_extra + [col_fecha] if col_fecha not in cols_fecha_extra else cols_fecha_extra
    
    for col in all_date_cols:
        if col in df.columns and col in columnas:
            # apply str (si es None queda 'None' o 'NaT' -> cuidado)
            # Mejor lambda seguro
            df[col] = df[col].apply(lambda x: x.isoformat() if x is not None and pd.notnull(x) else None)

    # Limpieza final de NaNs para JSON
    df_clean = df[columnas].where(pd.notnull(df[columnas]), None)
    registros = df_clean.to_dict("records")
    
    BATCH_SIZE = 1000 
    total_batches = (len(registros) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(registros), BATCH_SIZE):
        batch = registros[i:i+BATCH_SIZE]
        current_batch = i // BATCH_SIZE + 1
        
        try:
            supabase.table(tabla).insert(batch).execute()
            print(f"   ✅ Lote {current_batch}/{total_batches} procesado ({len(batch)} registros)")
            time.sleep(0.1) 
        except Exception as e:
            print(f"   ❌ Error subiendo lote {current_batch}: {e}")
            raise e

    print("🏁 Carga completada exitosamente")
