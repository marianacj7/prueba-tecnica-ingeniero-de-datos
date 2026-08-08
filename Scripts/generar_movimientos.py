import pandas as pd
import numpy as np
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


# Un único generador aleatorio para todo el script

rng = np.random.default_rng(SEED)


# Cantidad de movimientos a generar

TOTAL_MOVIMIENTOS = config["tablas"]["TB_MOV_FINANCIEROS"]["registros"]


# Rango de fechas

FECHA_INICIO = pd.Timestamp(
    config["tablas"]["TB_MOV_FINANCIEROS"]["fecha_inicio"]
)

FECHA_FIN = pd.Timestamp(
    config["tablas"]["TB_MOV_FINANCIEROS"]["fecha_fin"]
)

# ==========================================
# CARGAR TABLAS EXISTENTES
# ==========================================

clientes = pd.read_csv(
    "Data/TB_CLIENTES_CORE.csv"
)

productos = pd.read_csv(
    "Data/TB_PRODUCTOS_CAT.csv"
)

print("Clientes cargados:", len(clientes))
print("Productos cargados:", len(productos))


# ==========================================
# PREPARAR CLIENTES
# ==========================================

clientes["id_cli"] = clientes["id_cli"].astype(int)

clientes["ciudad_res"] = (
    clientes["ciudad_res"]
    .fillna("SIN_CIUDAD")
    .astype(str)
)


# ==========================================
# CREAR CÓDIGOS DE CIUDAD
# ==========================================

ciudades = sorted(
    clientes["ciudad_res"].unique()
)

mapa_ciudades = {
    ciudad: f"CIU{i:03d}"
    for i, ciudad in enumerate(
        ciudades,
        start=1
    )
}

clientes["cod_ciudad"] = (
    clientes["ciudad_res"]
    .map(mapa_ciudades)
)


# ==========================================
# CLASIFICAR PRODUCTOS
# ==========================================

productos["tip_prod"] = (
    productos["tip_prod"]
    .astype(str)
)

credito = productos[
    productos["tip_prod"] ==
    "Crédito de consumo"
].copy()

ahorro = productos[
    productos["tip_prod"] ==
    "Cuentas de ahorro digitales"
].copy()

transaccionales = productos[
    productos["tip_prod"] ==
    "Servicios transaccionales"
].copy()

print(
    "Productos de crédito:",
    len(credito)
)

print(
    "Productos de ahorro:",
    len(ahorro)
)

print(
    "Productos transaccionales:",
    len(transaccionales)
)


# ==========================================
# SELECCIONAR CLIENTES
# ==========================================

indices_clientes = rng.integers(
    0,
    len(clientes),
    size=TOTAL_MOVIMIENTOS
)

df_mov = clientes.iloc[
    indices_clientes
][
    [
        "id_cli",
        "cod_ciudad"
    ]
].reset_index(drop=True)


# ==========================================
# SELECCIONAR LÍNEA DE PRODUCTO
# ==========================================

lineas = rng.choice(
    [
        "Crédito de consumo",
        "Cuentas de ahorro digitales",
        "Servicios transaccionales"
    ],
    size=TOTAL_MOVIMIENTOS,
    p=[
        0.45,
        0.30,
        0.25
    ]
)

df_mov["linea"] = lineas


# ==========================================
# PREPARAR CÓDIGOS DE PRODUCTO
# ==========================================

codigos_credito = (
    credito["cod_prod"].tolist()
)

codigos_ahorro = (
    ahorro["cod_prod"].tolist()
)

codigos_transaccionales = (
    transaccionales["cod_prod"].tolist()
)


# ==========================================
# ASIGNAR PRODUCTOS
# ==========================================

df_mov["cod_prod"] = ""


for linea in [
    "Crédito de consumo",
    "Cuentas de ahorro digitales",
    "Servicios transaccionales"
]:

    mascara = (
        df_mov["linea"] == linea
    )

    cantidad = mascara.sum()

    if linea == "Crédito de consumo":

        productos_seleccionados = rng.choice(
            codigos_credito,
            size=cantidad
        )

    elif linea == "Cuentas de ahorro digitales":

        productos_seleccionados = rng.choice(
            codigos_ahorro,
            size=cantidad
        )

    else:

        productos_seleccionados = rng.choice(
            codigos_transaccionales,
            size=cantidad
        )

    df_mov.loc[
        mascara,
        "cod_prod"
    ] = productos_seleccionados


# ==========================================
# GENERAR FECHAS
# ==========================================

dias_periodo = (
    FECHA_FIN - FECHA_INICIO
).days + 1

dias_aleatorios = rng.integers(
    0,
    dias_periodo,
    size=TOTAL_MOVIMIENTOS
)

df_mov["fec_mov"] = (
    FECHA_INICIO
    + pd.to_timedelta(
        dias_aleatorios,
        unit="D"
    )
)


# ==========================================
# GENERAR HORARIOS
# ==========================================

horas = np.arange(24)

pesos_horas = np.array([
    0.01,
    0.01,
    0.01,
    0.01,
    0.01,
    0.01,
    0.02,
    0.04,
    0.06,
    0.07,
    0.07,
    0.08,
    0.08,
    0.07,
    0.06,
    0.05,
    0.05,
    0.06,
    0.08,
    0.08,
    0.06,
    0.04,
    0.03,
    0.02
])

pesos_horas = (
    pesos_horas /
    pesos_horas.sum()
)

horas_generadas = rng.choice(
    horas,
    size=TOTAL_MOVIMIENTOS,
    p=pesos_horas
)

minutos_generados = rng.integers(
    0,
    60,
    size=TOTAL_MOVIMIENTOS
)

segundos_generados = rng.integers(
    0,
    60,
    size=TOTAL_MOVIMIENTOS
)

df_mov["hra_mov"] = [
    f"{h:02d}:{m:02d}:{s:02d}"
    for h, m, s in zip(
        horas_generadas,
        minutos_generados,
        segundos_generados
    )
]


# ==========================================
# TIPOS DE MOVIMIENTO
# ==========================================

tipos = []

for linea in df_mov["linea"]:

    if linea == "Crédito de consumo":

        tipo = rng.choice(
            [
                "DESEMBOLSO",
                "PAGO_CREDITO",
                "COMPRA"
            ],
            p=[
                0.10,
                0.35,
                0.55
            ]
        )

    elif linea == "Cuentas de ahorro digitales":

        tipo = rng.choice(
            [
                "DEPOSITO",
                "RETIRO",
                "TRANSFERENCIA",
                "PAGO"
            ],
            p=[
                0.20,
                0.20,
                0.35,
                0.25
            ]
        )

    else:

        tipo = rng.choice(
            [
                "PAGO_PSE",
                "TRANSFERENCIA_ACH",
                "CORRESPONSALIA"
            ],
            p=[
                0.45,
                0.35,
                0.20
            ]
        )

    tipos.append(tipo)

df_mov["tip_mov"] = tipos


# ==========================================
# CANALES
# ==========================================

canales = []

for tipo in df_mov["tip_mov"]:

    if tipo == "PAGO_PSE":

        canal = rng.choice(
            [
                "PSE",
                "APP",
                "WEB"
            ],
            p=[
                0.65,
                0.20,
                0.15
            ]
        )

    elif tipo == "TRANSFERENCIA_ACH":

        canal = rng.choice(
            [
                "APP",
                "WEB",
                "ACH"
            ],
            p=[
                0.50,
                0.25,
                0.25
            ]
        )

    elif tipo == "CORRESPONSALIA":

        canal = "CORRESPONSALIA"

    elif tipo == "COMPRA":

        canal = rng.choice(
            [
                "APP",
                "WEB",
                "CORRESPONSALIA"
            ],
            p=[
                0.60,
                0.30,
                0.10
            ]
        )

    else:

        canal = rng.choice(
            [
                "APP",
                "WEB",
                "CORRESPONSALIA",
                "PSE"
            ],
            p=[
                0.45,
                0.25,
                0.15,
                0.15
            ]
        )

    canales.append(canal)

df_mov["cod_canal"] = canales


# ==========================================
# MONTOS
# ==========================================

montos = []

for tipo in df_mov["tip_mov"]:

    if tipo == "DESEMBOLSO":

        monto = rng.lognormal(
            mean=8.5,
            sigma=0.8
        )

    elif tipo == "PAGO_CREDITO":

        monto = rng.lognormal(
            mean=5.5,
            sigma=0.7
        )

    elif tipo == "COMPRA":

        monto = rng.lognormal(
            mean=4.0,
            sigma=0.8
        )

    elif tipo == "DEPOSITO":

        monto = rng.lognormal(
            mean=5.5,
            sigma=0.8
        )

    elif tipo == "RETIRO":

        monto = rng.lognormal(
            mean=4.5,
            sigma=0.7
        )

    elif tipo == "TRANSFERENCIA":

        monto = rng.lognormal(
            mean=6.0,
            sigma=0.9
        )

    elif tipo == "PAGO":

        monto = rng.lognormal(
            mean=4.5,
            sigma=0.7
        )

    elif tipo == "PAGO_PSE":

        monto = rng.lognormal(
            mean=4.5,
            sigma=0.8
        )

    elif tipo == "TRANSFERENCIA_ACH":

        monto = rng.lognormal(
            mean=6.0,
            sigma=0.9
        )

    else:

        monto = rng.lognormal(
            mean=4.2,
            sigma=0.7
        )

    montos.append(
        round(
            max(
                1,
                monto
            ),
            2
        )
    )

df_mov["vr_mov"] = montos


# ==========================================
# ESTADO DEL MOVIMIENTO
# ==========================================

df_mov["cod_estado_mov"] = rng.choice(
    [
        "APROBADA",
        "RECHAZADA",
        "REVERSADA"
    ],
    size=TOTAL_MOVIMIENTOS,
    p=[
        0.94,
        0.04,
        0.02
    ]
)


# ==========================================
# NÚMERO DE CUENTA
# ==========================================

codigo_linea = {
    "Crédito de consumo": "CR",
    "Cuentas de ahorro digitales": "AH",
    "Servicios transaccionales": "TR"
}

df_mov["num_cuenta"] = [
    (
        f"{codigo_linea[linea]}"
        f"{int(id_cli):08d}"
    )
    for id_cli, linea in zip(
        df_mov["id_cli"],
        df_mov["linea"]
    )
]


# ==========================================
# DISPOSITIVOS
# ==========================================

numero_dispositivo = rng.integers(
    1,
    4,
    size=TOTAL_MOVIMIENTOS
)

df_mov["id_dispositivo"] = [
    f"DEV{int(id_cli):08d}_{int(num)}"
    for id_cli, num in zip(
        df_mov["id_cli"],
        numero_dispositivo
    )
]


# ==========================================
# ID DE MOVIMIENTO
# ==========================================

df_mov.insert(
    0,
    "id_mov",
    np.arange(
        1,
        TOTAL_MOVIMIENTOS + 1
    )
)


# ==========================================
# ANOMALÍA 1:
# FECHAS FUERA DE RANGO
# ==========================================

indices_fechas = rng.choice(
    TOTAL_MOVIMIENTOS - 30,
    size=30,
    replace=False
)

dias_anomalia = rng.integers(
    1,
    61,
    size=30
)

for indice, dias in zip(
    indices_fechas,
    dias_anomalia
):

    df_mov.loc[
        indice,
        "fec_mov"
    ] = (
        FECHA_INICIO
        - pd.Timedelta(
            days=int(dias)
        )
    )


# ==========================================
# ANOMALÍA 2:
# MONTOS ATÍPICOS
# ==========================================

indices_montos = rng.choice(
    TOTAL_MOVIMIENTOS - 30,
    size=30,
    replace=False
)

montos_anomalos = rng.uniform(
    500000,
    1000000,
    size=30
)

for indice, monto in zip(
    indices_montos,
    montos_anomalos
):

    df_mov.loc[
        indice,
        "vr_mov"
    ] = round(
        float(monto),
        2
    )


# ==========================================
# 5 % DE NULOS CONTROLADOS
# ==========================================

cantidad_nulos = int(
    TOTAL_MOVIMIENTOS * 0.05
)

indices_nulos = rng.choice(
    TOTAL_MOVIMIENTOS - 30,
    size=cantidad_nulos,
    replace=False
)

df_mov.loc[
    indices_nulos,
    "id_dispositivo"
] = None


# ==========================================
# ANOMALÍA 3:
# TRANSACCIONES DUPLICADAS
# ==========================================

columnas_negocio = [
    "id_cli",
    "cod_prod",
    "num_cuenta",
    "fec_mov",
    "hra_mov",
    "vr_mov",
    "tip_mov",
    "cod_canal",
    "cod_ciudad",
    "cod_estado_mov",
    "id_dispositivo"
]


# Buscar registros únicos entre los primeros
# 499.970 registros.

indices_disponibles = (
    df_mov.iloc[
        :TOTAL_MOVIMIENTOS - 30
    ]
    .loc[
        df_mov.iloc[
            :TOTAL_MOVIMIENTOS - 30
        ]["id_dispositivo"].notna()
    ]
    .drop_duplicates(
        subset=columnas_negocio
    )
    .index
    .to_numpy()
)

indices_duplicados = rng.choice(
    indices_disponibles,
    size=30,
    replace=False
)


# Copiar los 30 registros seleccionados
# en las últimas 30 posiciones.

for i, indice_original in enumerate(
    indices_duplicados
):

    nuevo_indice = (
        TOTAL_MOVIMIENTOS
        - 30
        + i
    )

    for columna in columnas_negocio:

        df_mov.loc[
            nuevo_indice,
            columna
        ] = df_mov.loc[
            indice_original,
            columna
        ]


# ==========================================
# ELIMINAR COLUMNA AUXILIAR
# ==========================================

df_mov = df_mov.drop(
    columns=["linea"]
)


# ==========================================
# FORMATO DE FECHAS
# ==========================================

df_mov["fec_mov"] = (
    pd.to_datetime(
        df_mov["fec_mov"]
    ).dt.strftime(
        "%Y-%m-%d"
    )
)


# ==========================================
# VALIDACIONES
# ==========================================

print("\nPrimeros registros:")

print(
    df_mov.head()
)


print("\nTotal de movimientos:")

print(
    len(df_mov)
)


print("\nValores nulos:")

print(
    df_mov.isnull().sum()
)


print("\nClientes inexistentes:")

print(
    (
        ~df_mov["id_cli"].isin(
            clientes["id_cli"]
        )
    ).sum()
)


print("\nProductos inexistentes:")

print(
    (
        ~df_mov["cod_prod"].isin(
            productos["cod_prod"]
        )
    ).sum()
)


print(
    "\nDistribución por tipo de movimiento:"
)

print(
    df_mov["tip_mov"].value_counts()
)


print(
    "\nDistribución por canal:"
)

print(
    df_mov["cod_canal"].value_counts()
)


print("\nEstados:")

print(
    df_mov["cod_estado_mov"].value_counts()
)


print("\nFechas mínimas y máximas:")

print(
    df_mov["fec_mov"].min(),
    df_mov["fec_mov"].max()
)


print("\nDuplicados de negocio:")

print(
    df_mov.duplicated(
        subset=columnas_negocio
    ).sum()
)


print("\nMovimientos fuera del rango:")

print(
    (
        (
            pd.to_datetime(
                df_mov["fec_mov"]
            )
            < FECHA_INICIO
        )
        |
        (
            pd.to_datetime(
                df_mov["fec_mov"]
            )
            > FECHA_FIN
        )
    ).sum()
)


print(
    "\nMovimientos con monto atípico intencional:"
)

print(
    (
        df_mov["vr_mov"] >= 500000
    ).sum()
)


# ==========================================
# EXPORTAR CSV
# ==========================================

df_mov.to_csv(
    "Data/TB_MOV_FINANCIEROS.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# EXPORTAR JSON
# ==========================================

df_mov.to_json(
    "Data/TB_MOV_FINANCIEROS.json",
    orient="records",
    indent=4,
    force_ascii=False
)


print(
    "\nArchivos guardados correctamente."
)