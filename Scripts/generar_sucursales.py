import pandas as pd
import random
import json


# ==========================================
# CONFIGURACIÓN
# ==========================================

# Cargar configuración centralizada

with open(
    "config/parametros_generacion.json",
    "r",
    encoding="utf-8"
) as archivo:

    config = json.load(archivo)


# Semilla para reproducibilidad

SEED = config["seed"]

random.seed(SEED)


# Cantidad de sucursales a generar

TOTAL_SUCURSALES = config["tablas"]["TB_SUCURSALES_RED"]["registros"]

# ==========================================
# CARGAR CLIENTES
# ==========================================

clientes = pd.read_csv(
    "Data/TB_CLIENTES_CORE.csv"
)


# ==========================================
# CIUDADES Y COORDENADAS DE REFERENCIA
# ==========================================

coordenadas = {
    "Bogotá": (4.7110, -74.0721),
    "Medellín": (6.2442, -75.5812),
    "Cali": (3.4516, -76.5320),
    "Barranquilla": (10.9685, -74.7813),
    "Cartagena": (10.3910, -75.4794),

    "Ciudad de México": (19.4326, -99.1332),
    "Guadalajara": (20.6597, -103.3496),
    "Monterrey": (25.6866, -100.3161),
    "Puebla": (19.0414, -98.2063),
    "Querétaro": (20.5888, -100.3899),

    "Lima": (-12.0464, -77.0428),
    "Arequipa": (-16.4090, -71.5375),
    "Trujillo": (-8.1116, -79.0287),
    "Cusco": (-13.5319, -71.9675),

    "Santiago": (-33.4489, -70.6693),
    "Valparaíso": (-33.0472, -71.6127),
    "Concepción": (-36.8201, -73.0444),

    "Buenos Aires": (-34.6037, -58.3816),
    "Córdoba": (-31.4201, -64.1888),
    "Rosario": (-32.9442, -60.6505)
}


# ==========================================
# CIUDADES EXISTENTES EN TB_CLIENTES_CORE
# ==========================================

ciudades_clientes = (
    clientes[
        ["ciudad_res", "depto_res"]
    ]
    .drop_duplicates()
    .rename(
        columns={
            "ciudad_res": "ciudad",
            "depto_res": "depto"
        }
    )
)


# Mantener únicamente ciudades para las
# cuales tenemos coordenadas de referencia

ciudades_disponibles = ciudades_clientes[
    ciudades_clientes["ciudad"].isin(
        coordenadas.keys()
    )
].copy()


print(
    "Ciudades disponibles:",
    len(ciudades_disponibles)
)


# ==========================================
# FUNCIÓN PARA GENERAR UNA SUCURSAL
# ==========================================

def generar_sucursal(
    cod_suc,
    ciudad,
    depto
):

    # Coordenadas de referencia de la ciudad
    lat_base, lon_base = coordenadas[
        ciudad
    ]

    # Pequeña variación para que los puntos
    # de una misma ciudad no tengan exactamente
    # las mismas coordenadas.

    latitud = (
        lat_base +
        random.uniform(
            -0.05,
            0.05
        )
    )

    longitud = (
        lon_base +
        random.uniform(
            -0.05,
            0.05
        )
    )

    # Tipo de punto de atención
    tipo_punto = random.choices(
        [
            "SUCURSAL",
            "CORRESPONSAL"
        ],
        weights=[
            60,
            40
        ],
        k=1
    )[0]

    # Estado del punto
    activo = random.choices(
        [
            "ACTIVO",
            "INACTIVO"
        ],
        weights=[
            90,
            10
        ],
        k=1
    )[0]

    # Nombre del punto
    nom_suc = (
        f"FinBank {tipo_punto.title()} "
        f"{ciudad} {cod_suc}"
    )

    return {
        "cod_suc": cod_suc,
        "nom_suc": nom_suc,
        "tip_punto": tipo_punto,
        "ciudad": ciudad,
        "depto": depto,
        "latitud": round(
            latitud,
            6
        ),
        "longitud": round(
            longitud,
            6
        ),
        "activo": activo
    }


# ==========================================
# GENERAR 200 SUCURSALES
# ==========================================

sucursales = []

for numero in range(
    1,
    TOTAL_SUCURSALES + 1
):

    # Seleccionar una ciudad existente
    indice = random.randrange(
        len(ciudades_disponibles)
    )

    ciudad_info = (
        ciudades_disponibles.iloc[
            indice
        ]
    )

    ciudad = ciudad_info[
        "ciudad"
    ]

    depto = ciudad_info[
        "depto"
    ]

    cod_suc = (
        f"SUC{numero:04d}"
    )

    sucursal = generar_sucursal(
        cod_suc,
        ciudad,
        depto
    )

    sucursales.append(
        sucursal
    )


# ==========================================
# CREAR DATAFRAME
# ==========================================

df_sucursales = pd.DataFrame(
    sucursales
)


# ==========================================
# VALIDACIONES
# ==========================================

print("\nPrimeros registros:")

print(
    df_sucursales.head()
)


print("\nTotal de sucursales:")

print(
    len(df_sucursales)
)


print("\nCódigos duplicados:")

print(
    df_sucursales[
        "cod_suc"
    ].duplicated().sum()
)


print("\nCiudades:")

print(
    df_sucursales[
        "ciudad"
    ].value_counts()
)


print("\nTipos de punto:")

print(
    df_sucursales[
        "tip_punto"
    ].value_counts()
)


print("\nEstados:")

print(
    df_sucursales[
        "activo"
    ].value_counts()
)


print("\nValores nulos:")

print(
    df_sucursales.isnull().sum()
)


# ==========================================
# EXPORTAR CSV
# ==========================================

df_sucursales.to_csv(
    "Data/TB_SUCURSALES_RED.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# EXPORTAR JSON
# ==========================================

df_sucursales.to_json(
    "Data/TB_SUCURSALES_RED.json",
    orient="records",
    indent=4,
    force_ascii=False
)

print(
    "\nArchivos guardados correctamente."
)