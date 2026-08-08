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


# Cantidad de obligaciones a generar

TOTAL_OBLIGACIONES = config["tablas"]["TB_OBLIGACIONES"]["registros"]

# ==========================================
# CARGAR TABLAS EXISTENTES
# ==========================================

clientes = pd.read_csv(
    "Data/TB_CLIENTES_CORE.csv"
)

productos = pd.read_csv(
    "Data/TB_PRODUCTOS_CAT.csv"
)

# Convertir fecha de alta del cliente
clientes["fec_alta"] = pd.to_datetime(
    clientes["fec_alta"]
)


# ==========================================
# FILTRAR PRODUCTOS DE CRÉDITO
# ==========================================

productos_credito = productos[
    productos["tip_prod"] == "Crédito de consumo"
].copy()

print("Clientes cargados:", len(clientes))
print("Productos de crédito:", len(productos_credito))


# ==========================================
# FUNCIÓN PARA GENERAR UNA OBLIGACIÓN
# ==========================================

def generar_obligacion(id_oblig, cliente, producto):

    # --------------------------------------
    # INFORMACIÓN DEL CLIENTE
    # --------------------------------------

    id_cli = cliente["id_cli"]
    segmento = cliente["cod_segmento"]
    score = cliente["score_buro"]
    fec_alta = cliente["fec_alta"]

    # --------------------------------------
    # INFORMACIÓN DEL PRODUCTO
    # --------------------------------------

    cod_prod = producto["cod_prod"]
    desc_prod = producto["desc_prod"]

    tasa_ea = producto["tasa_ea"]
    plazo_max_meses = producto["plazo_max_meses"]

    # ======================================
    # MONTO APROBADO SEGÚN PRODUCTO Y SEGMENTO
    # ======================================

    if "Crédito de libre inversión" in desc_prod:

        if segmento == "BAS":
            vr_aprobado = random.uniform(500, 5000)

        elif segmento == "STD":
            vr_aprobado = random.uniform(5000, 20000)

        elif segmento == "PRE":
            vr_aprobado = random.uniform(20000, 50000)

        else:
            vr_aprobado = random.uniform(50000, 100000)

    elif "Crédito rotativo" in desc_prod:

        if segmento == "BAS":
            vr_aprobado = random.uniform(500, 3000)

        elif segmento == "STD":
            vr_aprobado = random.uniform(3000, 10000)

        elif segmento == "PRE":
            vr_aprobado = random.uniform(10000, 25000)

        else:
            vr_aprobado = random.uniform(25000, 50000)

    else:
        # Tarjeta digital

        if segmento == "BAS":
            vr_aprobado = random.uniform(300, 2000)

        elif segmento == "STD":
            vr_aprobado = random.uniform(2000, 8000)

        elif segmento == "PRE":
            vr_aprobado = random.uniform(8000, 20000)

        else:
            vr_aprobado = random.uniform(20000, 40000)

    vr_aprobado = round(vr_aprobado, 2)


    # ======================================
    # VALOR DESEMBOLSADO
    # ======================================

    if random.random() < 0.90:

        vr_desembolsado = vr_aprobado

    else:

        vr_desembolsado = (
            vr_aprobado *
            random.uniform(0.80, 0.99)
        )

    vr_desembolsado = round(
        vr_desembolsado,
        2
    )


    # ======================================
    # FECHA DE DESEMBOLSO
    # Nunca puede ser anterior al alta
    # del cliente
    # ======================================

    fecha_hoy = pd.Timestamp.today().normalize()

    dias_disponibles = (
        fecha_hoy - fec_alta
    ).days

    if dias_disponibles > 0:

        dias_desembolso = random.randint(
            0,
            dias_disponibles
        )

        fec_desembolso = (
            fec_alta +
            pd.Timedelta(
                days=dias_desembolso
            )
        )

    else:

        fec_desembolso = fec_alta


    # ======================================
    # PLAZO DEL PRODUCTO
    # ======================================

    if pd.notna(plazo_max_meses):

        plazo_meses = int(
            plazo_max_meses
        )

    else:

        # Crédito rotativo y tarjeta digital
        # no tienen plazo contractual fijo.
        #
        # Se utiliza un horizonte técnico
        # de 12 meses para calcular los
        # campos derivados.

        plazo_meses = 12


    # ======================================
    # FECHA DE VENCIMIENTO
    # ======================================

    fec_venc = (
        fec_desembolso +
        pd.DateOffset(
            months=plazo_meses
        )
    )


    # ======================================
    # ANTIGÜEDAD DEL CRÉDITO
    # ======================================

    meses_transcurridos = (
        (fecha_hoy.year - fec_desembolso.year) * 12
        + (
            fecha_hoy.month -
            fec_desembolso.month
        )
    )

    meses_transcurridos = max(
        0,
        min(
            meses_transcurridos,
            plazo_meses
        )
    )


    # ======================================
    # CUOTAS PENDIENTES
    # ======================================

    num_cuotas_pend = max(
        0,
        plazo_meses - meses_transcurridos
    )


    # ======================================
    # CUOTA
    # ======================================

    if "Crédito de libre inversión" in desc_prod:

        vr_cuota = (
            vr_desembolsado /
            plazo_meses
        )

    else:

        # Para crédito rotativo y tarjeta
        # se utiliza una cuota equivalente
        # al 5 % del valor desembolsado.

        vr_cuota = (
            vr_desembolsado *
            0.05
        )

    vr_cuota = round(
        vr_cuota,
        2
    )


    # ======================================
    # DÍAS DE MORA
    # ======================================

    prob_mora = random.random()

    if prob_mora < 0.82:

        dias_mora_act = 0

    elif prob_mora < 0.90:

        dias_mora_act = random.randint(
            1,
            30
        )

    elif prob_mora < 0.95:

        dias_mora_act = random.randint(
            31,
            60
        )

    elif prob_mora < 0.98:

        dias_mora_act = random.randint(
            61,
            90
        )

    else:

        dias_mora_act = random.randint(
            91,
            180
        )


    # ======================================
    # SALDO DE CAPITAL
    # ======================================

    if dias_mora_act > 90:

        porcentaje_saldo = random.uniform(
            0.40,
            0.95
        )

    elif dias_mora_act > 0:

        porcentaje_saldo = random.uniform(
            0.30,
            0.85
        )

    else:

        porcentaje_saldo = random.uniform(
            0.05,
            0.80
        )

    sdo_capital = round(
        vr_desembolsado *
        porcentaje_saldo,
        2
    )


    # ======================================
    # CALIFICACIÓN DE RIESGO
    # ======================================

    if dias_mora_act > 90:

        calif_riesgo = "CRITICO"

    elif (
        dias_mora_act > 30
        or score < 550
    ):

        calif_riesgo = "ALTO"

    elif (
        score <= 700
        or dias_mora_act > 0
    ):

        calif_riesgo = "MEDIO"

    else:

        calif_riesgo = "BAJO"


    # ======================================
    # RETORNAR OBLIGACIÓN
    # ======================================

    return {
        "id_oblig": id_oblig,
        "id_cli": id_cli,
        "cod_prod": cod_prod,
        "vr_aprobado": vr_aprobado,
        "vr_desembolsado": vr_desembolsado,
        "sdo_capital": sdo_capital,
        "vr_cuota": vr_cuota,
        "fec_desembolso": fec_desembolso,
        "fec_venc": fec_venc,
        "dias_mora_act": dias_mora_act,
        "num_cuotas_pend": num_cuotas_pend,
        "calif_riesgo": calif_riesgo
    }


# ==========================================
# GENERAR LAS 30.000 OBLIGACIONES
# ==========================================

obligaciones = []

for id_oblig in range(
    1,
    TOTAL_OBLIGACIONES + 1
):

    # Seleccionar cliente usando el mismo
    # generador aleatorio controlado por seed
    indice_cliente = random.randrange(
        len(clientes)
    )

    cliente = clientes.iloc[
        indice_cliente
    ]

    # Seleccionar producto usando el mismo
    # generador aleatorio
    indice_producto = random.randrange(
        len(productos_credito)
    )

    producto = productos_credito.iloc[
        indice_producto
    ]

    obligacion = generar_obligacion(
        id_oblig,
        cliente,
        producto
    )

    obligaciones.append(
        obligacion
    )


# ==========================================
# CREAR DATAFRAME
# ==========================================

df_obligaciones = pd.DataFrame(
    obligaciones
)


# ==========================================
# ANOMALÍA INTENCIONAL
# ==========================================

# 20 obligaciones tendrán un valor
# desembolsado superior al aprobado.

indices_anomalia = random.sample(
    range(
        len(df_obligaciones)
    ),
    20
)

for indice in indices_anomalia:

    df_obligaciones.loc[
        indice,
        "vr_desembolsado"
    ] = round(
        df_obligaciones.loc[
            indice,
            "vr_aprobado"
        ] * 1.10,
        2
    )


# ==========================================
# 5 % DE VALORES NULOS CONTROLADOS
# ==========================================

# Se simula una calificación de riesgo
# pendiente de actualización.

cantidad_nulos = int(
    len(df_obligaciones) * 0.05
)

indices_nulos = random.sample(
    range(
        len(df_obligaciones)
    ),
    cantidad_nulos
)

df_obligaciones.loc[
    indices_nulos,
    "calif_riesgo"
] = None


# ==========================================
# FORMATO DE FECHAS
# ==========================================

df_obligaciones["fec_desembolso"] = (
    pd.to_datetime(
        df_obligaciones[
            "fec_desembolso"
        ]
    ).dt.strftime(
        "%Y-%m-%d"
    )
)

df_obligaciones["fec_venc"] = (
    pd.to_datetime(
        df_obligaciones[
            "fec_venc"
        ]
    ).dt.strftime(
        "%Y-%m-%d"
    )
)


# ==========================================
# VALIDACIONES
# ==========================================

print("\nPrimeros registros:")

print(
    df_obligaciones.head()
)


print("\nTotal de obligaciones:")

print(
    len(df_obligaciones)
)


print("\nValores nulos:")

print(
    df_obligaciones.isnull().sum()
)


print("\nProductos:")

print(
    df_obligaciones[
        "cod_prod"
    ].value_counts()
)


print("\nDistribución de mora:")

print(
    pd.cut(
        df_obligaciones[
            "dias_mora_act"
        ],
        bins=[
            -1,
            0,
            30,
            60,
            90,
            float("inf")
        ],
        labels=[
            "Al día",
            "Rango 1",
            "Rango 2",
            "Rango 3",
            "Deteriorado"
        ]
    ).value_counts()
)


# ==========================================
# VALIDACIONES DE INTEGRIDAD
# ==========================================

print(
    "\nClientes inexistentes:",
    (
        ~df_obligaciones[
            "id_cli"
        ].isin(
            clientes["id_cli"]
        )
    ).sum()
)


print(
    "Productos inexistentes:",
    (
        ~df_obligaciones[
            "cod_prod"
        ].isin(
            productos["cod_prod"]
        )
    ).sum()
)


print(
    "Desembolsos mayores al aprobado:",
    (
        df_obligaciones[
            "vr_desembolsado"
        ]
        >
        df_obligaciones[
            "vr_aprobado"
        ]
    ).sum()
)


print(
    "Saldos mayores al desembolso:",
    (
        df_obligaciones[
            "sdo_capital"
        ]
        >
        df_obligaciones[
            "vr_desembolsado"
        ]
    ).sum()
)


print(
    "Desembolsos posteriores al vencimiento:",
    (
        pd.to_datetime(
            df_obligaciones[
                "fec_desembolso"
            ]
        )
        >
        pd.to_datetime(
            df_obligaciones[
                "fec_venc"
            ]
        )
    ).sum()
)


print(
    "Productos que no son de crédito:",
    (
        ~df_obligaciones[
            "cod_prod"
        ].isin(
            productos_credito[
                "cod_prod"
            ]
        )
    ).sum()
)


# ==========================================
# EXPORTAR CSV
# ==========================================

df_obligaciones.to_csv(
    "Data/TB_OBLIGACIONES.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# EXPORTAR JSON
# ==========================================

df_obligaciones.to_json(
    "Data/TB_OBLIGACIONES.json",
    orient="records",
    indent=4,
    force_ascii=False
)


print(
    "\nArchivos guardados correctamente."
)