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

rng = np.random.default_rng(SEED)


# Cantidad de comisiones a generar

TOTAL_COMISIONES = config["tablas"]["TB_COMISIONES_LOG"]["registros"]


# Rango de fechas

FECHA_INICIO = pd.Timestamp(
    config["tablas"]["TB_COMISIONES_LOG"]["fecha_inicio"]
)

FECHA_FIN = pd.Timestamp(
    config["tablas"]["TB_COMISIONES_LOG"]["fecha_fin"]
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
# PREPARAR TIPOS DE DATOS
# ==========================================

clientes["id_cli"] = (
    clientes["id_cli"].astype(int)
)

productos["comision_admin"] = pd.to_numeric(
    productos["comision_admin"],
    errors="coerce"
)


# ==========================================
# VALIDAR CATÁLOGO
# ==========================================

print("\nProductos con comisión administrativa:")

print(
    productos[
        [
            "cod_prod",
            "desc_prod",
            "tip_prod",
            "comision_admin"
        ]
    ].head(10)
)


productos_sin_comision = (
    productos["comision_admin"]
    .isna()
    .sum()
)

print(
    "\nProductos sin comisión administrativa:",
    productos_sin_comision
)


if productos_sin_comision > 0:

    raise ValueError(
        "Existen productos sin comision_admin. "
        "Revisar TB_PRODUCTOS_CAT."
    )


# ==========================================
# SEPARAR PRODUCTOS POR TIPO
# ==========================================

productos_credito = productos[
    productos["tip_prod"] ==
    "Crédito de consumo"
].copy()

productos_ahorro = productos[
    productos["tip_prod"] ==
    "Cuentas de ahorro digitales"
].copy()

productos_transaccionales = productos[
    productos["tip_prod"] ==
    "Servicios transaccionales"
].copy()


print(
    "\nProductos de crédito:",
    len(productos_credito)
)

print(
    "Productos de ahorro:",
    len(productos_ahorro)
)

print(
    "Productos transaccionales:",
    len(productos_transaccionales)
)


# ==========================================
# LISTAS DE PRODUCTOS
# ==========================================

codigos_credito = (
    productos_credito["cod_prod"]
    .tolist()
)

codigos_ahorro = (
    productos_ahorro["cod_prod"]
    .tolist()
)

codigos_transaccionales = (
    productos_transaccionales["cod_prod"]
    .tolist()
)


# ==========================================
# GENERAR CLIENTES
# ==========================================

ids_clientes = rng.choice(
    clientes["id_cli"].to_numpy(),
    size=TOTAL_COMISIONES,
    replace=True
)


# ==========================================
# GENERAR PRODUCTOS
# ==========================================

# Distribución:
# 40 % crédito
# 20 % ahorro
# 40 % transaccionales

tipo_producto = rng.choice(
    [
        "credito",
        "ahorro",
        "transaccional"
    ],
    size=TOTAL_COMISIONES,
    p=[
        0.40,
        0.20,
        0.40
    ]
)


codigos_producto = np.empty(
    TOTAL_COMISIONES,
    dtype=object
)


for tipo in [
    "credito",
    "ahorro",
    "transaccional"
]:

    mascara = (
        tipo_producto == tipo
    )

    cantidad = mascara.sum()

    if tipo == "credito":

        codigos = rng.choice(
            codigos_credito,
            size=cantidad
        )

    elif tipo == "ahorro":

        codigos = rng.choice(
            codigos_ahorro,
            size=cantidad
        )

    else:

        codigos = rng.choice(
            codigos_transaccionales,
            size=cantidad
        )

    codigos_producto[mascara] = codigos


# ==========================================
# OBTENER COMISIÓN DEL CATÁLOGO
# ==========================================

# Aquí relacionamos directamente:
#
# TB_COMISIONES_LOG.cod_prod
#          ↓
# TB_PRODUCTOS_CAT.cod_prod
#
# y obtenemos:
#
# TB_PRODUCTOS_CAT.comision_admin
#
# Este campo NO se guarda en la tabla final.

mapa_comisiones = (
    productos
    .set_index("cod_prod")[
        "comision_admin"
    ]
    .to_dict()
)


valores_comision = np.array(
    [
        mapa_comisiones[cod_prod]
        for cod_prod in codigos_producto
    ],
    dtype=float
)


# ==========================================
# GENERAR FECHAS
# ==========================================

dias_periodo = (
    FECHA_FIN - FECHA_INICIO
).days + 1


# Para evitar duplicados naturales,
# generamos combinaciones y las controlamos
# posteriormente.

dias = rng.integers(
    0,
    dias_periodo,
    size=TOTAL_COMISIONES
)


fechas = (
    FECHA_INICIO
    + pd.to_timedelta(
        dias,
        unit="D"
    )
)


# ==========================================
# TIPO DE COMISIÓN
# ==========================================

# La única tarifa de comisión definida
# explícitamente en TB_PRODUCTOS_CAT es
# comision_admin.
#
# Por eso no inventamos otros tipos de
# comisión ni tarifas adicionales.

tipos_comision = np.full(
    TOTAL_COMISIONES,
    "COMISION_ADMIN",
    dtype=object
)


# ==========================================
# ESTADO DEL COBRO
# ==========================================

estados = rng.choice(
    [
        "COBRADA",
        "PENDIENTE",
        "RECHAZADA"
    ],
    size=TOTAL_COMISIONES,
    p=[
        0.90,
        0.07,
        0.03
    ]
)


# ==========================================
# CONSTRUIR DATAFRAME
# ==========================================

df_com = pd.DataFrame(
    {
        "id_comision": np.arange(
            1,
            TOTAL_COMISIONES + 1
        ),

        "id_cli": ids_clientes,

        "cod_prod": codigos_producto,

        "fec_cobro": fechas,

        "vr_comision": valores_comision,

        "tip_comision": tipos_comision,

        "estado_cobro": estados
    }
)


# ==========================================
# GARANTIZAR QUE LOS REGISTROS NORMALES
# SEAN ÚNICOS
# ==========================================

columnas_negocio = [
    "id_cli",
    "cod_prod",
    "fec_cobro",
    "vr_comision",
    "tip_comision",
    "estado_cobro"
]


registros_usados = set()


for indice in range(
    TOTAL_COMISIONES
):

    while True:

        fila = df_com.loc[
            indice,
            columnas_negocio
        ]

        clave = tuple(
            fila.tolist()
        )

        if clave not in registros_usados:

            registros_usados.add(
                clave
            )

            break

        # Si ya existe la combinación,
        # cambiamos la fecha de cobro.

        fecha_actual = pd.Timestamp(
            df_com.loc[
                indice,
                "fec_cobro"
            ]
        )

        nueva_fecha = (
            fecha_actual
            + pd.Timedelta(
                days=1
            )
        )

        if nueva_fecha > FECHA_FIN:

            nueva_fecha = FECHA_INICIO

        df_com.loc[
            indice,
            "fec_cobro"
        ] = nueva_fecha


# ==========================================
# ANOMALÍA 1:
# FECHAS FUERA DEL RANGO
# ==========================================

indices_fechas = rng.choice(
    TOTAL_COMISIONES - 20,
    size=20,
    replace=False
)


dias_anomalia = rng.integers(
    1,
    61,
    size=20
)


for indice, dias_atras in zip(
    indices_fechas,
    dias_anomalia
):

    df_com.loc[
        indice,
        "fec_cobro"
    ] = (
        FECHA_INICIO
        - pd.Timedelta(
            days=int(dias_atras)
        )
    )


# ==========================================
# ANOMALÍA 2:
# COMISIONES INCONSISTENTES
# ==========================================

# Seleccionamos 20 registros que no sean
# parte de la anomalía de fechas.

indices_disponibles = [
    i
    for i in range(
        TOTAL_COMISIONES - 20
    )
    if i not in indices_fechas
]


indices_inconsistentes = rng.choice(
    indices_disponibles,
    size=20,
    replace=False
)


for indice in indices_inconsistentes:

    # Alteramos intencionalmente el valor
    # respecto al catálogo.

    df_com.loc[
        indice,
        "vr_comision"
    ] = (
        df_com.loc[
            indice,
            "vr_comision"
        ]
        + 1000
    )


# ==========================================
# 5 % DE NULOS CONTROLADOS
# ==========================================

cantidad_nulos = int(
    TOTAL_COMISIONES * 0.05
)


indices_nulos = rng.choice(
    [
        i
        for i in range(
            TOTAL_COMISIONES - 20
        )
        if i not in indices_fechas
        and i not in indices_inconsistentes
    ],
    size=cantidad_nulos,
    replace=False
)


# tip_comision es el campo no crítico
# seleccionado para los valores nulos.

df_com.loc[
    indices_nulos,
    "tip_comision"
] = None


# ==========================================
# ANOMALÍA 3:
# DUPLICADOS INTENCIONALES
# ==========================================

# Seleccionamos registros normales,
# sin nulos, sin inconsistencias y sin
# fechas fuera de rango.

indices_disponibles = [
    i
    for i in range(
        TOTAL_COMISIONES - 20
    )
    if i not in indices_fechas
    and i not in indices_inconsistentes
    and i not in indices_nulos
]


indices_duplicados = rng.choice(
    indices_disponibles,
    size=20,
    replace=False
)


# Los últimos 20 registros serán
# copias exactas de los seleccionados.

for posicion, indice_original in enumerate(
    indices_duplicados
):

    nuevo_indice = (
        TOTAL_COMISIONES
        - 20
        + posicion
    )

    for columna in columnas_negocio:

        df_com.loc[
            nuevo_indice,
            columna
        ] = df_com.loc[
            indice_original,
            columna
        ]


# ==========================================
# FORMATO FINAL
# ==========================================

df_com["fec_cobro"] = (
    pd.to_datetime(
        df_com["fec_cobro"]
    ).dt.strftime(
        "%Y-%m-%d"
    )
)


# ==========================================
# VALIDACIONES
# ==========================================

print("\nPrimeros registros:")

print(
    df_com.head()
)


print("\nTotal de comisiones:")

print(
    len(df_com)
)


print("\nValores nulos:")

print(
    df_com.isnull().sum()
)


# ==========================================
# INTEGRIDAD REFERENCIAL
# ==========================================

print("\nClientes inexistentes:")

print(
    (
        ~df_com["id_cli"].isin(
            clientes["id_cli"]
        )
    ).sum()
)


print("\nProductos inexistentes:")

print(
    (
        ~df_com["cod_prod"].isin(
            productos["cod_prod"]
        )
    ).sum()
)


# ==========================================
# VALIDAR COHERENCIA CON EL CATÁLOGO
# ==========================================

df_validacion = df_com.merge(
    productos[
        [
            "cod_prod",
            "comision_admin"
        ]
    ],
    on="cod_prod",
    how="left",
    validate="many_to_one"
)


# Solo evaluamos los registros que tienen
# COMISION_ADMIN y no son nulos.

mascara_validacion = (
    df_validacion["tip_comision"]
    == "COMISION_ADMIN"
)


inconsistencias = (
    (
        df_validacion.loc[
            mascara_validacion,
            "vr_comision"
        ]
        !=
        df_validacion.loc[
            mascara_validacion,
            "comision_admin"
        ]
    )
).sum()


print(
    "\nComisiones inconsistentes con el catálogo:"
)

print(
    inconsistencias
)


# ==========================================
# DISTRIBUCIÓN POR TIPO
# ==========================================

print(
    "\nDistribución por tipo de comisión:"
)

print(
    df_com[
        "tip_comision"
    ].value_counts(
        dropna=False
    )
)


# ==========================================
# DISTRIBUCIÓN POR ESTADO
# ==========================================

print(
    "\nDistribución por estado:"
)

print(
    df_com[
        "estado_cobro"
    ].value_counts()
)


# ==========================================
# FECHAS
# ==========================================

print(
    "\nFechas mínimas y máximas:"
)

print(
    df_com["fec_cobro"].min(),
    df_com["fec_cobro"].max()
)


# ==========================================
# DUPLICADOS
# ==========================================

print(
    "\nDuplicados de negocio:"
)

print(
    df_com.duplicated(
        subset=columnas_negocio
    ).sum()
)


# ==========================================
# FECHAS FUERA DEL RANGO
# ==========================================

print(
    "\nComisiones fuera del rango:"
)

print(
    (
        (
            pd.to_datetime(
                df_com["fec_cobro"]
            )
            < FECHA_INICIO
        )
        |
        (
            pd.to_datetime(
                df_com["fec_cobro"]
            )
            > FECHA_FIN
        )
    ).sum()
)


# ==========================================
# COMISIONES EFECTIVAMENTE COBRADAS
# ==========================================

print(
    "\nComisiones efectivamente cobradas:"
)

print(
    (
        df_com[
            "estado_cobro"
        ]
        == "COBRADA"
    ).sum()
)


# ==========================================
# EXPORTAR CSV
# ==========================================

df_com.to_csv(
    "Data/TB_COMISIONES_LOG.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# EXPORTAR JSON
# ==========================================

df_com.to_json(
    "Data/TB_COMISIONES_LOG.json",
    orient="records",
    indent=4,
    force_ascii=False
)


print(
    "\nArchivos guardados correctamente."
)