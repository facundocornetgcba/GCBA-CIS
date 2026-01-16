"""
Script de Mantenimiento: Eliminar Duplicados en Supabase
"""
import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

TABLAS_CLAVES = {
    "cis_registros": ["nro_documento", "fecha_ingreso"],
    "cis_info": ["fecha", "nombre_cis"]
}

def clean_duplicates(tabla, claves):
    print(f"🧹 Analizando tabla '{tabla}'...")
    
    # 1. Traer todos los IDs y Claves
    # Seleccionamos id_registro (o equivalente PK) y las claves
    # Necesitamos saber el nombre de la PK. Asumimos 'id' o buscamos columna única.
    # En cis_registros parece ser 'id_registro'? En cis_info?
    # Haremos un fetch de 1 row para ver la PK o asumimos columnas.
    
    print(f"   📥 Descargando registros de '{tabla}' (paginación)...")
    
    all_data = []
    start = 0
    BATCH_FETCH = 1000
    
    while True:
        try:
            # Paginación usando range
            response = supabase.table(tabla)\
                .select("*")\
                .range(start, start + BATCH_FETCH - 1)\
                .execute()
            
            batch = response.data
            if not batch:
                break
                
            all_data.extend(batch)
            print(f"      Leídos {len(all_data)}...")
            
            if len(batch) < BATCH_FETCH:
                break
                
            start += BATCH_FETCH
        except Exception as e:
            print(f"      ❌ Error descargando: {e}")
            break
    
    data = all_data
    
    if not data:
        print("   Vacía.")
        return

    df = pd.DataFrame(data)
    print(f"   Total registros analizados: {len(df)}")
    
    # Normalizar claves para detección
    for k in claves:
        df[k] = df[k].astype(str).str.strip()
    
    # Identificar duplicados
    # keep='first' marca todos menos la primera ocurrencia como True (duplicado)
    # Asumimos que queremos borrar los extras.
    # Para ser deterministicos, ordenamos por 'created_at' o lo que sea.
    if "created_at" in df.columns:
        df = df.sort_values("created_at", ascending=True) 
        # keep='first' mantiene el MAS ANTIGUO. 
        # Si queremos mantener el más nuevo, sort ascending=False o keep='last'.
        # Generalmente mantenemos el primero insertado.
    
    dups = df[df.duplicated(subset=claves, keep='first')]
    
    if dups.empty:
        print("   ✅ No hay duplicados.")
        return

    print(f"   ⚠️ Encontrados {len(dups)} duplicados para borrar.")
    
    # Asumimos que hay una columna 'id' única generada por Supabase (o id_registro)
    # Si no hay ID, es difícil borrar específico.
    # Busquemos candidatos a ID
    posibles_id = [c for c in df.columns if "id" in c.lower()]
    pk = "id" 
    if "id_registro" in df.columns: 
        pk = "id_registro"
    elif posibles_id:
        pk = posibles_id[0]
    
    print(f"   Usando columna '{pk}' como identificador para borrar.")
    
    ids_to_delete = dups[pk].tolist()
    
    # Borrar en batches
    BATCH = 100
    for i in range(0, len(ids_to_delete), BATCH):
        batch_ids = ids_to_delete[i:i+BATCH]
        try:
            supabase.table(tabla).delete().in_(pk, batch_ids).execute()
            print(f"   🗑️ Borrados {len(batch_ids)} registros...")
        except Exception as e:
            print(f"   ❌ Error borrando: {e}")

    print("   ✨ Limpieza finalizada.")

for t, k in TABLAS_CLAVES.items():
    clean_duplicates(t, k)
