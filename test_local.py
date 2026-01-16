"""
Script de prueba local para el pipeline ETL
Ejecuta solo Extract y Transform (sin cargar a Supabase)
"""
from config.settings import CONFIG_HOJAS, HOJAS_GID, BASE_DIR
from extract.sheets import read_sheet
from transform.normalizacion import procesar_hoja
import pandas as pd

print("🚀 Iniciando prueba local del pipeline ETL\n")
print("=" * 60)

for hoja, cfg in CONFIG_HOJAS.items():
    print(f"\n📋 Procesando hoja: {hoja}")
    print("-" * 60)
    
    # EXTRACT
    try:
        df = read_sheet(hoja, HOJAS_GID[hoja])
        print(f"   ✅ Extracción exitosa")
        print(f"   📊 Columnas: {list(df.columns)}")
        print(f"   📏 Dimensiones: {df.shape}")
    except Exception as e:
        print(f"   ❌ Error en extracción: {e}")
        continue
    
    # TRANSFORM
    try:
        ruta_limpio = procesar_hoja(hoja, df, cfg, BASE_DIR)
        print(f"   ✅ Transformación exitosa")
        print(f"   💾 Archivo guardado en: {ruta_limpio}")
        
        # Verificar el archivo generado
        df_limpio = pd.read_parquet(ruta_limpio)
        print(f"   📊 Registros finales: {len(df_limpio)}")
        print(f"   📋 Columnas finales: {list(df_limpio.columns)}")
        
        # Mostrar primeras filas
        print(f"\n   🔍 Primeras 3 filas:")
        print(df_limpio.head(3).to_string(index=False))
        
    except Exception as e:
        print(f"   ❌ Error en transformación: {e}")
        import traceback
        traceback.print_exc()
        continue

print("\n" + "=" * 60)
print("🏁 Prueba local finalizada")
print(f"📁 Archivos generados en: {BASE_DIR}")
