import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


# ============================================
# CONFIGURACIÓN
# ============================================

SERVIDOR = "servidor-prueba-datos-mcj.database.windows.net"
BASE_DATOS = "db-prueba-ingeniero-datos"
USUARIO = "adminprueba"


# ============================================
# AZURE KEY VAULT
# ============================================

KEY_VAULT_URL = "https://kv-prueba-datos-mcj-2026.vault.azure.net/"

credential = DefaultAzureCredential()

secret_client = SecretClient(
    vault_url=KEY_VAULT_URL,
    credential=credential
)

# Obtener la contraseña desde Azure Key Vault
CONTRASENA = secret_client.get_secret(
    "sql-admin-password"
).value


# ============================================
# CONEXIÓN A AZURE SQL
# ============================================

ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

cadena_conexion = (
    f"DRIVER={{{ODBC_DRIVER}}};"
    f"SERVER={SERVIDOR};"
    f"DATABASE={BASE_DATOS};"
    f"UID={USUARIO};"
    f"PWD={CONTRASENA};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

cadena_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(cadena_conexion)
)

engine = create_engine(
    cadena_url,
    fast_executemany=True
)


# ============================================
# PRUEBA DE CONEXIÓN
# ============================================

print("\nProbando conexión con Azure SQL...")

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Conexión exitosa a Azure SQL Database.")

except Exception as e:
    print("\nERROR DE CONEXIÓN:")
    print(e)
    raise


# ============================================
# TABLAS A CARGAR
# ============================================

tablas = {
    "TB_CLIENTES_CORE": "Data/TB_CLIENTES_CORE.csv",
    "TB_PRODUCTOS_CAT": "Data/TB_PRODUCTOS_CAT.csv",
    "TB_OBLIGACIONES": "Data/TB_OBLIGACIONES.csv",
    "TB_SUCURSALES_RED": "Data/TB_SUCURSALES_RED.csv",
    "TB_MOV_FINANCIEROS": "Data/TB_MOV_FINANCIEROS.csv",
    "TB_COMISIONES_LOG": "Data/TB_COMISIONES_LOG.csv"
}


# ============================================
# CARGAR TABLAS
# ============================================

for nombre_tabla, ruta_archivo in tablas.items():

    print("\n" + "=" * 60)
    print(f"Cargando: {nombre_tabla}")
    print(f"Archivo: {ruta_archivo}")
    print("=" * 60)

    df = pd.read_csv(ruta_archivo)

    print(f"Registros encontrados: {len(df):,}")

    df.to_sql(
        nombre_tabla,
        con=engine,
        schema="dbo",
        if_exists="replace",
        index=False,
        chunksize=5000
    )

    print(f"{nombre_tabla} cargada correctamente.")


# ============================================
# FINALIZACIÓN
# ============================================

print("\n" + "=" * 60)
print("CARGA COMPLETADA")
print("=" * 60)

print(f"Base de datos: {BASE_DATOS}")
print("Todas las tablas fueron cargadas correctamente.")