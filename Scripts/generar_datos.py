# ===========================================
# PRUEBA TÉCNICA - INGENIERÍA DE DATOS
# Proyecto: FinBank S.A.
# Generación de datos sintéticos
# ===========================================

# ==========================
# IMPORTAR LIBRERÍAS
# ==========================

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import json

# Crear generador de datos en español
fake = Faker(["es_MX", "es_CO"])


# Cargar configuración

with open(
    "config/parametros_generacion.json",
    "r",
    encoding="utf-8"
) as archivo:
    config = json.load(archivo)


# Semilla para que los datos sean reproducibles

SEED = config["seed"]

random.seed(SEED)
Faker.seed(SEED)

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================

# Número de clientes a generar

NUM_CLIENTES = config["tablas"]["TB_CLIENTES_CORE"]["registros"]

# ==========================
# CATÁLOGOS
# ==========================

# Distribución de clientes por país
PAISES = {
    "Colombia": 45,
    "México": 25,
    "Perú": 12,
    "Chile": 10,
    "Argentina": 8
}

# Segmentación de clientes
SEGMENTOS = {
    "BAS": 45,
    "STD": 35,
    "PRE": 15,
    "ELI": 5
}

# Estado del cliente
ESTADOS_CLIENTE = {
    "ACTIVO": 94,
    "INACTIVO": 5,
    "BLOQUEADO": 1
}

# Canal de adquisición
CANALES = {
    "APP": 65,
    "WEB": 25,
    "CORRESPONSAL": 10
}

# Tipo de documento
TIPOS_DOCUMENTO = {
    "IDNAL": 85,
    "PASP": 10,
    "CE": 5
}

# ==========================
# CATÁLOGO DE CIUDADES
# ==========================

CIUDADES = {

    "Colombia": {
        "Bogotá": {
            "departamento": "Cundinamarca",
            "peso": 40
        },
        "Medellín": {
            "departamento": "Antioquia",
            "peso": 30
        },
        "Cali": {
            "departamento": "Valle del Cauca",
            "peso": 20
        },
        "Barranquilla": {
            "departamento": "Atlántico",
            "peso": 10
        }
    },

    "México": {
        "Ciudad de México": {
            "departamento": "Ciudad de México",
            "peso": 45
        },
        "Guadalajara": {
            "departamento": "Jalisco",
            "peso": 30
        },
        "Monterrey": {
            "departamento": "Nuevo León",
            "peso": 25
        }
    },

    "Perú": {
        "Lima": {
            "departamento": "Lima",
            "peso": 75
        },
        "Arequipa": {
            "departamento": "Arequipa",
            "peso": 25
        }
    },

    "Chile": {
        "Santiago": {
            "departamento": "Región Metropolitana",
            "peso": 80
        },
        "Valparaíso": {
            "departamento": "Valparaíso",
            "peso": 20
        }
    },

    "Argentina": {
        "Buenos Aires": {
            "departamento": "Buenos Aires",
            "peso": 75
        },
        "Córdoba": {
            "departamento": "Córdoba",
            "peso": 25
        }
    }

}

# ===========================================
# FUNCIÓN PARA GENERAR UN CLIENTE
# ===========================================

def generar_cliente(id_cliente):

    # Tipo de documento
    tip_doc = random.choices(
        list(TIPOS_DOCUMENTO.keys()),
        weights=list(TIPOS_DOCUMENTO.values())
    )[0]

    # Segmento
    segmento = random.choices(
        list(SEGMENTOS.keys()),
        weights=list(SEGMENTOS.values())
    )[0]

    # Estado del cliente
    estado = random.choices(
        list(ESTADOS_CLIENTE.keys()),
        weights=list(ESTADOS_CLIENTE.values())
    )[0]

    # Canal de adquisición
    canal = random.choices(
        list(CANALES.keys()),
        weights=list(CANALES.values())
    )[0]

    # País
    pais = random.choices(
        list(PAISES.keys()),
        weights=list(PAISES.values())
    )[0]

    # Ciudad y departamento
    ciudades = list(CIUDADES[pais].keys())

    pesos = [CIUDADES[pais][c]["peso"] for c in ciudades]

    ciudad = random.choices(ciudades, weights=pesos)[0]

    departamento = CIUDADES[pais][ciudad]["departamento"]

    # Score según el segmento
    if segmento == "BAS":
        score = random.randint(300, 620)
    elif segmento == "STD":
        score = random.randint(550, 730)
    elif segmento == "PRE":
        score = random.randint(700, 850)
    elif segmento == "ELI":
        score = random.randint(820, 950)

    cliente = {

        "id_cli": id_cliente,

        "nomb_cli": fake.first_name(),

        "apell_cli": fake.last_name(),

        "tip_doc": tip_doc,

        "num_doc": fake.unique.random_number(digits=10),
        
        "fec_nac": fake.date_between(
            start_date="-85y",
            end_date="-18y"
        ),

        "fec_alta": fake.date_between(
            start_date="-11y",
            end_date="today"
        ),

        "cod_segmento": segmento,

        "score_buro": score,

        "ciudad_res": ciudad,

        "depto_res": departamento,

        "estado_cli": estado,

        "canal_adquis": canal

    }

    return cliente

# ===========================================
# GENERAR TABLA DE CLIENTES
# ===========================================
# ===========================================
# GENERAR TABLA TB_CLIENTES_CORE
# ===========================================

clientes = []

for i in range(1, 10001):
    clientes.append(generar_cliente(i))

df_clientes = pd.DataFrame(clientes)

# Exportar a CSV
df_clientes.to_csv(
    "Data/TB_CLIENTES_CORE.csv",
    index=False,
    encoding="utf-8-sig"    
)

# Exportar a JSON
df_clientes.to_json(
    "Data/TB_CLIENTES_CORE.json",
    orient="records",
    indent=4,
    force_ascii=False
)

print("\nPrimeros registros:")
print(df_clientes.head())

print("\nTotal de clientes:")
print(len(df_clientes))

print("TB_CLIENTES_CORE creada correctamente.")