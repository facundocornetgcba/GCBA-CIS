import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ==============================
# GLOBAL
# ==============================
BASE_DIR = os.getenv("BASE_DIR", "./data")
PRIMERA_CARGA = False

SHEET_ID = "1Xk7GHICWrUOi2-sNaEl7TPnHyZIBp7S9O4iEZl15_Uc"

HOJAS_GID = {
    "Datos": "149047211",
    "Info_CIS": "1838984784"
}

CONFIG_HOJAS = {
    "Datos": {
        "columnas_limpio": [
            "fecha_ingreso",
            "fecha_egreso",
            "nro_documento",
            "fecha_nac",
            "tipo_egreso",
            "subtipo_egreso",
            "poblacion_cis",
            "genero",
            "nombre_cis",
            "categoria_cis",
            "fecha_carga"
        ],
        "columnas_fecha": [
            "fecha_ingreso",
            "fecha_egreso",
            "fecha_nac"
        ],
        "clave_negocio": ["nro_documento", "fecha_ingreso"]
    },

    "Info_CIS": {
        "columnas_limpio": [
            "fecha",
            "nombre_cis",
            "tipo_cis",
            "plazas_total",
            "plazas_ocupadas",
            "plazas_libres",
            "poblacion_cis",
            "fecha_carga"
        ],
        "columnas_fecha": ["fecha"],
        "clave_negocio": ["fecha", "nombre_cis"]
    }
}
