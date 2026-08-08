import pandas as pd

# Leer catálogo maestro
df_productos = pd.read_excel("Data/TB_PRODUCTOS_CAT.xlsx")

# Exportar a CSV
df_productos.to_csv(
    "Data/TB_PRODUCTOS_CAT.csv",
    index=False,
    encoding="utf-8-sig"
)

# Exportar a JSON
df_productos.to_json(
    "Data/TB_PRODUCTOS_CAT.json",
    orient="records",
    indent=4,
    force_ascii=False
)

print(df_productos.head())
print("Archivo guardado correctamente")

# ==========================
# VALIDACIONES
# ==========================

# print(df_productos.isnull().sum())

# print(df_productos["estado_prod"].value_counts())

# print(df_productos["tip_prod"].value_counts())

# print(df_productos[df_productos["plazo_max_meses"].isnull()][["desc_prod","tip_prod"]])

# print(df_productos[df_productos["cuota_min"].isnull()][["desc_prod","tip_prod"]])