# Prueba Técnica – Ingeniería de Datos

## Candidata
Mariana Cifuentes Jaramillo

## Sector
Banca y Servicios Financieros

## Plataforma cloud seleccionada
- Microsoft Azure

## Justificación de la plataforma seleccionada

Para el desarrollo de esta prueba se seleccionó **Microsoft Azure** como plataforma cloud principal.

La solución se implementará de forma consistente utilizando servicios del ecosistema Azure, de acuerdo con los lineamientos establecidos en la prueba técnica.

### Razones de la elección

- Azure ofrece una interfaz intuitiva y amigable, facilitando la administración de los recursos durante el desarrollo del proyecto.
- Integra en un mismo ecosistema los servicios necesarios para almacenamiento, bases de datos, procesamiento y análisis de datos, permitiendo construir una solución completa de principio a fin.
- Cuenta con una integración natural con SQL y con el ecosistema Microsoft, facilitando el desarrollo de soluciones de datos.
- Es una de las plataformas cloud más utilizadas en entornos empresariales, especialmente por organizaciones que utilizan tecnologías Microsoft.

## Justificación del sector seleccionado

Seleccioné el sector de **Banca y Servicios Financieros** debido a mi experiencia profesional en esta industria, lo que me permite comprender mejor sus procesos, terminología y necesidades de negocio.

He trabajado con la gestión de información financiera, procesos operativos y análisis de datos, lo que me ha permitido comprender la importancia de la calidad, la precisión y la trazabilidad de la información en este tipo de organizaciones.

Además, conozco la importancia de automatizar procesos que permitan optimizar la operación y garantizar información confiable para la toma de decisiones. Considero que el sector financiero representa un escenario ideal para aplicar una solución de ingeniería de datos, debido al alto volumen de información que se procesa y a la necesidad de mantener datos precisos, consistentes y seguros.

Por estas razones, considero que este sector me permitirá desarrollar una solución alineada tanto con mi experiencia como con los objetivos planteados en la prueba técnica.

## Problema Identificado 

Actualmente el área de Riesgo Crediticio y el área de Prevención de Fraude dependen de procesos manuales basados en múltiples fuentes de información desconectadas. Esto genera retrasos en la disponibilidad de los datos, inconsistencias entre reportes y un mayor riesgo operativo. Adicionalmente, la ausencia de una fuente consolidada dificulta el análisis histórico requerido para fortalecer los modelos y reglas de detección de fraude.

La solución propuesta busca centralizar la información proveniente de las diferentes fuentes del banco en una única plataforma de datos, permitiendo que las áreas de Riesgo Crediticio, Prevención de Fraude, Comercial y Cumplimiento regulatorio consulten información consistente, actualizada y confiable para la toma de decisiones.

## Generación Datos  

Para la generación de los datos sintéticos se seleccionó **Python** como lenguaje de programación, debido a su amplia adopción en proyectos de ingeniería de datos, su facilidad para automatizar procesos y la disponibilidad de librerías especializadas para la generación, transformación y manipulación de datos.

Python permitió desarrollar un proceso reproducible, flexible y fácilmente escalable para la creación de las tablas del modelo relacional, cumpliendo con los requisitos planteados en la prueba técnica.

### Herramientas utilizadas

Durante la generación de los datos sintéticos se utilizaron las siguientes librerías de Python:

- **Faker:** utilizada para generar información sintética como nombres, apellidos, fechas y documentos de identificación.
- **Pandas:** utilizada para almacenar temporalmente la información en DataFrames, validar la estructura de los datos y exportar las tablas a los formatos CSV y JSON.
- **Random:** utilizada para controlar las distribuciones de probabilidad (segmentos, países, tipos de documento, etc.) y para garantizar la reproducibilidad mediante una semilla fija.
- **Datetime:** utilizada para la generación y manipulación de fechas de alta y fechas de nacimiento.

## Generación de la tabla `TB_CLIENTES_CORE`

La tabla **TB_CLIENTES_CORE** fue desarrollada en Python utilizando la librería **Faker** para generar datos sintéticos. Se configuró una semilla fija (`random.seed(42)` y `Faker.seed(42)`) para garantizar que la generación de los datos sea reproducible en cada ejecución del script.

Durante el diseño de la tabla se tomaron las siguientes decisiones técnicas:

### Distribución geográfica

FinBank opera en cinco países de Latinoamérica: **Colombia, México, Perú, Chile y Argentina**. Por esta razón se decidió generar clientes pertenecientes a los cinco países, asignando una distribución ponderada para representar una mayor concentración de clientes en Colombia y México y una menor participación en los demás países.

Para simplificar el modelo sin perder realismo, se seleccionó un conjunto de las principales ciudades de cada país, asignando también diferentes pesos de distribución con el fin de reflejar una mayor concentración de clientes en las ciudades con mayor población.

### Generación de nombres

Se utilizó Faker con los locales **es_CO** y **es_MX** para generar nombres y apellidos más representativos de Latinoamérica. Esta configuración permite obtener datos más acordes con el contexto del banco, evitando nombres propios de España que no reflejan el escenario planteado.

### Tipo de documento

Debido a que cada uno de los cinco países utiliza una nomenclatura distinta para sus documentos de identidad, se optó por utilizar códigos genéricos comunes para toda la base de datos:

- **IDNAL**: Documento de identidad nacional.
- **PASP**: Pasaporte.
- **CE**: Documento para extranjeros.

Esta decisión permite mantener un modelo homogéneo para todos los países sin depender de la legislación o nomenclatura específica de cada uno.

### Segmentación de clientes

Los clientes fueron distribuidos de acuerdo con los segmentos definidos en el caso de negocio:

- BAS (Básico): 45 %
- STD (Estándar): 35 %
- PRE (Premium): 15 %
- ELI (Elite): 5 %

Esta distribución busca representar una mayor proporción de clientes de los segmentos básico y estándar, mientras que los segmentos premium y elite corresponden a una menor participación dentro de la cartera.

### Score crediticio

El score de buró se generó de forma coherente con el segmento del cliente, asignando rangos de puntaje progresivamente mayores para los segmentos de mayor valor:

| Segmento | Rango de score |
|----------|---------------:|
| BAS | 300 - 620 |
| STD | 550 - 730 |
| PRE | 700 - 850 |
| ELI | 820 - 950 |

De esta forma, los clientes pertenecientes a segmentos superiores presentan, en promedio, un mejor comportamiento crediticio.

### Fechas de alta

Las fechas de alta de los clientes se generaron desde el año 2015, que fue el año de fundación de FinBank hasta la fecha actual, permitiendo representar tanto clientes antiguos como clientes recientemente incorporados al banco.

### Formatos de salida

Con el fin de simular un escenario de ingesta heterogénea, la tabla se exporta en dos formatos:

- CSV
- JSON

Con ello se cumple el requisito de generar los datos en múltiples formatos de salida.

## Generación de la tabla `TB_PRODUCTOS_CAT`

La tabla **TB_PRODUCTOS_CAT** corresponde al catálogo maestro de productos ofrecidos por FinBank y constituye la base para la relación entre clientes, productos, obligaciones y transacciones en las etapas posteriores del proyecto.

Para la generación del catálogo se tomó como referencia el modelo de negocio descrito en el caso de estudio, respetando las tres líneas de producto definidas para la entidad:

- Crédito de consumo.
- Cuentas de ahorro digitales.
- Servicios transaccionales.

### Modelado del catálogo de productos

La línea de **Crédito de consumo** se compone de los siguientes productos base:

- Crédito de libre inversión.
- Crédito rotativo.
- Tarjeta digital.

La línea de **Cuentas de ahorro digitales** se representa mediante el producto:

- Cuenta de ahorro digital.

La línea de **Servicios transaccionales** incluye:

- Pago PSE.
- Transferencia ACH.
- Corresponsalía.

Aunque el caso de negocio define siete productos principales, la tabla requiere un catálogo de cincuenta registros. Para cumplir este requisito sin alterar el modelo funcional de FinBank, se construyeron diferentes variantes comerciales de cada producto, manteniendo siempre las tres líneas de negocio definidas en el caso. De esta manera, se evita incorporar productos que no hacen parte del alcance planteado y se obtiene un catálogo más cercano al utilizado por una entidad financiera real.

### Hipótesis de modelado

El caso de negocio no especifica una moneda de referencia para la operación multinacional de FinBank. Por esta razón, todos los valores monetarios del proyecto se expresan en **dólares estadounidenses (USD)**, permitiendo mantener un criterio homogéneo para la generación de datos sintéticos y facilitar el análisis entre los diferentes países donde opera la entidad.

De igual forma, la clasificación de clientes en los segmentos **Básico**, **Estándar**, **Premium** y **Elite** se mantuvo conforme a las reglas establecidas en el caso de negocio. Para efectos de la simulación, se asumió una unidad de referencia común para los rangos de ingreso asociados a cada segmento, dado que el caso no define salarios mínimos ni monedas específicas por país.

### Construcción del catálogo maestro

A diferencia de las tablas transaccionales, **TB_PRODUCTOS_CAT** fue construida como un **catálogo maestro**, por lo que sus atributos no fueron generados de forma aleatoria. Se elaboró manualmente un archivo de referencia (`TB_PRODUCTOS_CAT.xlsx`) que contiene la definición de cada producto y sus características financieras.

Posteriormente, el script desarrollado en Python utiliza la librería **Pandas** para leer este catálogo y generar los archivos de salida en los formatos requeridos (CSV y JSON), preservando la estructura definida en el archivo maestro.

### Criterios de negocio utilizados

Las condiciones financieras de cada producto fueron definidas de acuerdo con su naturaleza y comportamiento esperado dentro de una entidad financiera.

- **Créditos de libre inversión:** se asignaron tasas de interés entre el 12 % y el 28 % efectivo anual, con plazos máximos entre 24 y 84 meses. Los productos con mejores condiciones comerciales presentan tasas más bajas y mayores plazos, mientras que modalidades como Express tienen tasas más altas y plazos más cortos.

- **Créditos rotativos:** se definieron tasas entre el 24 % y el 30 % efectivo anual. Debido a que este producto funciona mediante un cupo rotativo y no posee un plazo contractual fijo, el campo `plazo_max_meses` se dejó sin valor (NULL).

- **Tarjetas digitales:** se asignaron tasas diferenciadas según la categoría de la tarjeta (Clásica, Gold, Platinum, Black, entre otras). Al igual que el crédito rotativo, no se definió un plazo máximo por tratarse de un producto de cupo renovable.

- **Cuentas de ahorro digitales:** se establecieron tasas entre el 1 % y el 5 % efectivo anual, representando el rendimiento que el banco reconoce al cliente por sus depósitos. Estos productos no poseen plazo máximo ni cuota mínima.

- **Servicios transaccionales:** los productos de esta línea (Pago PSE, Transferencia ACH y Corresponsalía) no generan intereses ni contemplan plazos. Únicamente se definieron comisiones de acuerdo con el tipo de servicio prestado.

### Valores nulos

Los campos `plazo_max_meses` y `cuota_min` contienen valores nulos únicamente cuando dichos atributos no aplican al tipo de producto, como ocurre con las cuentas de ahorro digitales y los servicios transaccionales. Estos valores no representan errores de calidad de datos, sino una decisión de modelado consistente con las características de cada producto.

### Validaciones realizadas

Una vez generado el catálogo se verificó:

- Existencia de los 50 registros solicitados.
- Distribución de productos por línea de negocio.
- Distribución de estados del producto.
- Presencia de valores nulos únicamente en los campos donde el atributo no aplica.
- Exportación correcta de la información a los formatos CSV y JSON.

## Generación de la tabla `TB_OBLIGACIONES`

La tabla **TB_OBLIGACIONES** representa las obligaciones crediticias de los clientes de FinBank y permite modelar la cartera sobre la cual posteriormente se calcularán indicadores de mora, riesgo y rentabilidad.

La tabla contiene **30.000 registros** y se relaciona directamente con las tablas `TB_CLIENTES_CORE` y `TB_PRODUCTOS_CAT` mediante los campos `id_cli` y `cod_prod`, respectivamente.

### Relación con clientes y productos

Cada obligación se asigna a un cliente existente en `TB_CLIENTES_CORE`, utilizando su información de segmento, score de buró y fecha de alta como referencia para la generación de los datos.

De igual manera, cada obligación se relaciona con un producto existente en `TB_PRODUCTOS_CAT`. Para esta tabla únicamente se utilizan productos pertenecientes a la línea **Crédito de consumo**, ya que son los productos que generan una obligación financiera y pueden presentar saldo, cuotas y días de mora.

Los productos considerados corresponden a las variantes definidas previamente en el catálogo para:

- Crédito de libre inversión.
- Crédito rotativo.
- Tarjeta digital.

De esta manera, no se generan códigos de producto independientes ni valores que no existan previamente en el catálogo maestro.

### Criterios de generación

Los montos de las obligaciones se expresan en **dólares estadounidenses (USD)**, manteniendo la hipótesis de moneda común definida para el proyecto.

El valor aprobado se determina de acuerdo con el tipo de producto y el segmento del cliente. Se establecieron rangos diferentes para los segmentos **Básico (BAS), Estándar (STD), Premium (PRE) y Elite (ELI)**, buscando representar una mayor capacidad de crédito en los segmentos de mayores ingresos.

El `vr_desembolsado` se genera a partir del valor aprobado, manteniendo normalmente el mismo valor y permitiendo en una proporción menor desembolsos inferiores al monto aprobado.

El `sdo_capital` se mantiene siempre por debajo o igual al valor desembolsado. Su comportamiento se relaciona con los días de mora, permitiendo representar diferentes niveles de saldo pendiente en la cartera.

### Fechas y plazo

La fecha de desembolso se genera siempre a partir de la fecha de alta del cliente, evitando que una obligación sea creada antes de que el cliente exista en la entidad.

El campo `plazo_max_meses` se toma directamente de `TB_PRODUCTOS_CAT`, manteniendo la lógica definida para cada producto. A partir de este valor se calcula la fecha de vencimiento y el número de cuotas pendientes.

Para productos cuyo catálogo no define un plazo contractual fijo, se utiliza un horizonte técnico de **12 meses** únicamente para realizar los cálculos derivados necesarios para la simulación.

### Mora y riesgo

Los días de mora se generaron utilizando una distribución no uniforme, buscando representar una cartera predominantemente al día y una proporción menor de obligaciones con diferentes niveles de deterioro.

La clasificación utilizada corresponde a los rangos establecidos en las reglas de negocio:

- **Al día:** 0 días.
- **Rango 1:** 1–30 días.
- **Rango 2:** 31–60 días.
- **Rango 3:** 61–90 días.
- **Deteriorado:** más de 90 días.

La calificación de riesgo se determina considerando conjuntamente el `score_buro` del cliente y los días de mora de la obligación, generando las categorías **BAJO, MEDIO, ALTO y CRITICO**.

Esta estructura permitirá posteriormente construir el campo calculado `bucket_mora` requerido para los indicadores de cartera.

### Calidad de datos y anomalías

Para cumplir con el requisito de simular condiciones reales de calidad de datos, se incorporó aproximadamente un **5 % de valores nulos controlados** en el campo `calif_riesgo`, simulando registros cuya clasificación de riesgo se encuentra pendiente de actualización.

También se incorporaron **20 anomalías intencionales** en las que el `vr_desembolsado` supera el `vr_aprobado`. Estas anomalías serán utilizadas posteriormente para probar las reglas de calidad y detección del pipeline.

### Validaciones realizadas

Antes de exportar la información se realizaron las siguientes validaciones:

- Todos los `id_cli` de las obligaciones existen en `TB_CLIENTES_CORE`.
- Todos los `cod_prod` existen en `TB_PRODUCTOS_CAT`.
- Todos los productos utilizados pertenecen a la línea Crédito de consumo.
- No existen saldos de capital superiores al valor desembolsado.
- No existen fechas de desembolso posteriores a la fecha de vencimiento.
- Se verificó la presencia de las 20 anomalías intencionales.
- Se verificó el 5 % de valores nulos en `calif_riesgo`.

Los resultados obtenidos fueron:

| Validación | Resultado |
|---|---:|
| Registros generados | 30.000 |
| Clientes inexistentes | 0 |
| Productos inexistentes | 0 |
| Productos que no son de crédito | 0 |
| Saldos mayores al desembolso | 0 |
| Desembolsos posteriores al vencimiento | 0 |
| Anomalías `vr_desembolsado > vr_aprobado` | 20 |
| Nulos en `calif_riesgo` | 1.500 (5 %) |

### Generación consistente de datos

La generación se realiza mediante el script `Scripts/generar_obligaciones.py` utilizando una **semilla aleatoria fija (`random.seed(42)`)**.

Esto permite obtener los mismos datos cada vez que el script se ejecuta bajo las mismas condiciones. Esta característica fue comprobada mediante dos ejecuciones consecutivas del script, verificando que los registros generados y los resultados obtenidos fueran iguales.

### Formatos de salida

La tabla se exporta en dos formatos para cumplir con el requisito de ingesta heterogénea:

```text
Data/TB_OBLIGACIONES.csv
Data/TB_OBLIGACIONES.json

## Generación de la tabla `TB_SUCURSALES_RED`

La tabla **TB_SUCURSALES_RED** representa la red de puntos de atención de FinBank y contiene información geográfica y operativa de las sucursales y corresponsales de la entidad.

La tabla contiene **200 registros** y está compuesta por los siguientes campos:

- `cod_suc`: código único del punto de atención.
- `nom_suc`: nombre del punto de atención.
- `tip_punto`: tipo de punto de atención.
- `ciudad`: ciudad donde se encuentra ubicado.
- `depto`: departamento o división geográfica asociada.
- `latitud`: coordenada geográfica de referencia.
- `longitud`: coordenada geográfica de referencia.
- `activo`: estado operativo del punto.

### Criterios de generación

La información se generó mediante el script `Scripts/generar_sucursales.py`.

Para mantener la consistencia geográfica del modelo, las ciudades y departamentos se tomaron como referencia de las ciudades existentes en `TB_CLIENTES_CORE`. De esta manera, la red de puntos de atención utiliza una geografía coherente con la base de clientes y puede relacionarse posteriormente con los movimientos financieros y los indicadores por ciudad.

Las coordenadas de latitud y longitud corresponden a valores de referencia de cada ciudad. Para permitir que diferentes puntos de una misma ciudad tengan ubicaciones distintas, se aplicó una pequeña variación alrededor de las coordenadas base.

### Tipos de punto

De acuerdo con el modelo de negocio de FinBank, se utilizaron dos tipos de puntos de atención:

- **Sucursal:** punto de atención física de la entidad.
- **Corresponsal:** punto aliado que permite realizar operaciones y servicios transaccionales.

La distribución generada fue:

| Tipo de punto | Registros |
|---|---:|
| Sucursal | 125 |
| Corresponsal | 75 |
| **Total** | **200** |

### Estado de los puntos

La mayoría de los puntos se encuentran activos, permitiendo representar una red operativa con algunos puntos que pueden encontrarse fuera de operación.

La distribución generada fue:

| Estado | Registros |
|---|---:|
| ACTIVO | 174 |
| INACTIVO | 26 |
| **Total** | **200** |

### Calidad de datos

Para esta tabla no se incorporaron valores nulos, debido a que todos los campos definidos son necesarios para identificar, ubicar y clasificar un punto de atención.

La validación realizada mostró:

| Campo | Valores nulos |
|---|---:|
| `cod_suc` | 0 |
| `nom_suc` | 0 |
| `tip_punto` | 0 |
| `ciudad` | 0 |
| `depto` | 0 |
| `latitud` | 0 |
| `longitud` | 0 |
| `activo` | 0 |

También se verificó que los códigos de sucursal fueran únicos y que la tabla contara con los **200 registros** requeridos.

### Generación consistente de datos

La generación se realiza utilizando una **semilla aleatoria fija (`random.seed(42)`)**, lo que permite obtener los mismos datos cada vez que el script se ejecuta bajo las mismas condiciones.

La consistencia fue comprobada mediante dos ejecuciones consecutivas del script, verificando que los resultados obtenidos fueran iguales.

### Formatos de salida

La tabla se exporta en dos formatos para cumplir con el requisito de ingesta heterogénea:

```text
Data/TB_SUCURSALES_RED.csv
Data/TB_SUCURSALES_RED.json

## Generación de la tabla `TB_MOV_FINANCIEROS`

La tabla **TB_MOV_FINANCIEROS** contiene el registro histórico de movimientos financieros realizados por los clientes de FinBank y constituye una de las principales tablas de hechos del modelo.

La tabla contiene **500.000 registros** y está compuesta por los siguientes campos:

- `id_mov`: identificador único del movimiento.
- `id_cli`: identificador del cliente que realiza la operación.
- `cod_prod`: código del producto asociado al movimiento.
- `num_cuenta`: número de cuenta asociado a la operación.
- `fec_mov`: fecha en la que se realizó el movimiento.
- `hra_mov`: hora en la que se realizó el movimiento.
- `vr_mov`: valor monetario del movimiento, expresado en USD.
- `tip_mov`: tipo de movimiento realizado.
- `cod_canal`: canal utilizado para realizar la operación.
- `cod_ciudad`: código de la ciudad asociada al cliente.
- `cod_estado_mov`: estado de la transacción.
- `id_dispositivo`: identificador del dispositivo utilizado.

### Relación con las tablas existentes

La generación de los movimientos se realizó tomando como referencia las tablas previamente construidas, con el objetivo de mantener la integridad referencial del modelo.

El campo `id_cli` se obtiene exclusivamente de los clientes existentes en `TB_CLIENTES_CORE`, mientras que `cod_prod` se obtiene de `TB_PRODUCTOS_CAT`.

Para los movimientos se utilizaron las tres líneas de producto definidas para FinBank:

- Crédito de consumo.
- Cuentas de ahorro digitales.
- Servicios transaccionales.

La distribución utilizada fue aproximadamente:

- 45 % para crédito de consumo.
- 30 % para cuentas de ahorro digitales.
- 25 % para servicios transaccionales.

El campo `cod_ciudad` se construyó a partir de las ciudades existentes en `TB_CLIENTES_CORE`, asignando un código único a cada ciudad para mantener una relación consistente con la información geográfica del cliente.

### Generación de cuentas y dispositivos

Debido a que el modelo de datos proporcionado no incluye una tabla independiente de cuentas, el campo `num_cuenta` se generó de manera sintética a partir del cliente y la línea de producto.

Se utilizaron prefijos diferentes según la línea:

- `CR`: Crédito de consumo.
- `AH`: Cuentas de ahorro digitales.
- `TR`: Servicios transaccionales.

Los dispositivos también fueron generados de forma sintética mediante identificadores asociados al cliente y a un número de dispositivo.

### Distribuciones de los datos

Los movimientos no fueron generados mediante una distribución completamente uniforme. Se aplicaron diferentes probabilidades según el tipo de producto y operación para representar un comportamiento más cercano al de una entidad financiera.

Los montos (`vr_mov`) fueron generados mediante distribuciones lognormales con parámetros diferentes según el tipo de movimiento. Todos los valores monetarios se expresan en **USD**.

Para la hora de la operación (`hra_mov`) se asignaron mayores probabilidades a las horas de mayor actividad, buscando representar una mayor concentración de transacciones durante horarios habituales de operación.

Los estados de las transacciones se distribuyeron entre:

- `APROBADA`
- `RECHAZADA`
- `REVERSADA`

### Cobertura temporal

Los datos cubren un periodo de **12 meses**, desde agosto de 2025 hasta julio de 2026.

El periodo permite generar el histórico necesario para los análisis de comportamiento de clientes y para la regla de detección de transacciones atípicas basada en el histórico de los últimos 30 días.

### Valores nulos controlados

De acuerdo con los requisitos del ejercicio, se incorporó aproximadamente un **5 % de valores nulos en un campo no crítico**.

El campo seleccionado fue `id_dispositivo`.

De los 500.000 movimientos generados:

- 25.000 registros tienen `id_dispositivo` nulo.
- Esto corresponde exactamente al **5 %** del total.

Los demás campos mantienen información completa debido a que son necesarios para las relaciones y análisis principales del modelo.

### Anomalías intencionales

Para cumplir con el requisito de calidad de datos, se incorporaron tres patrones de anomalías documentados.

#### 1. Transacciones duplicadas

Se generaron **30 transacciones duplicadas** utilizando como criterio de comparación los principales atributos de negocio del movimiento.

Estas anomalías permitirán probar posteriormente las reglas de detección y manejo de duplicados dentro del pipeline.

#### 2. Fechas fuera de rango

Se generaron **30 movimientos con fechas anteriores al periodo histórico definido**.

El periodo esperado comienza el:

`2025-08-01`

Los registros anómalos presentan fechas anteriores a este límite y permiten probar la detección de registros fuera del rango temporal esperado.

#### 3. Montos atípicos

Se generaron **30 movimientos con valores superiores o iguales a 500.000 USD**.

Estos registros fueron incorporados intencionalmente para representar comportamientos extremos y posteriormente permitir la validación de las reglas de detección de operaciones sospechosas.

### Validaciones realizadas

Durante la generación se realizaron validaciones de integridad y calidad de los datos:

| Validación | Resultado |
|---|---:|
| Total de movimientos | 500.000 |
| Clientes inexistentes | 0 |
| Productos inexistentes | 0 |
| Nulos en `id_dispositivo` | 25.000 |
| Duplicados intencionales | 30 |
| Movimientos fuera de rango | 30 |
| Montos atípicos intencionales | 30 |

La validación de integridad referencial confirmó que todos los valores de `id_cli` corresponden a clientes existentes y que todos los valores de `cod_prod` corresponden a productos registrados en `TB_PRODUCTOS_CAT`.

### Consistencia de la generación

Para garantizar que los datos puedan generarse nuevamente bajo las mismas condiciones, el script utiliza una semilla fija:

```python
SEED = 42
rng = np.random.default_rng(SEED)

Esto permite que las ejecuciones posteriores produzcan los mismos registros, distribuciones y anomalías bajo las mismas condiciones.

La consistencia fue comprobada ejecutando el script dos veces y verificando que los resultados obtenidos fueran iguales.

### Relación con las necesidades del negocio

`TB_MOV_FINANCIEROS` proporciona los datos necesarios para:

- Detectar transacciones con comportamiento atípico respecto al histórico del cliente.
- Analizar montos, frecuencia, canal y horario de las operaciones.
- Generar reportes regulatorios sobre cantidad y volumen de transacciones.
- Analizar volúmenes por canal y ciudad.
- Consolidar el nivel de uso de productos por cliente.
- Proporcionar información para posteriores análisis de rentabilidad y Customer Lifetime Value.

La bandera `ind_sospechoso` **no se genera directamente en esta tabla**, ya que la regla de negocio establece que debe calcularse posteriormente en la capa **Silver**, utilizando el promedio y la desviación estándar de los últimos 30 días del mismo cliente.

### Formatos de salida

La tabla se exporta en dos formatos para simular un escenario de ingesta heterogénea:

```text
Data/TB_MOV_FINANCIEROS.csv
Data/TB_MOV_FINANCIEROS.json

## Generación de la tabla `TB_COMISIONES_LOG`

La tabla **TB_COMISIONES_LOG** registra las comisiones asociadas a los productos de los clientes y permite identificar cuáles fueron efectivamente cobradas. Esta información será utilizada posteriormente para el cálculo del **Customer Lifetime Value (CLTV)**.

La tabla contiene **80.000 registros** y está compuesta por los siguientes campos:

- `id_comision`: identificador único de la comisión.
- `id_cli`: identificador del cliente asociado a la comisión.
- `cod_prod`: código del producto asociado.
- `fec_cobro`: fecha en la que se registra el cobro de la comisión.
- `vr_comision`: valor de la comisión, expresado en USD.
- `tip_comision`: tipo de comisión.
- `estado_cobro`: estado del cobro de la comisión.

### Relación con las tablas existentes

La generación de `TB_COMISIONES_LOG` utiliza información de las tablas previamente construidas para mantener la consistencia del modelo.

El campo `id_cli` se obtiene exclusivamente de `TB_CLIENTES_CORE`, garantizando que cada comisión esté asociada a un cliente existente.

El campo `cod_prod` se obtiene de `TB_PRODUCTOS_CAT`, garantizando que las comisiones estén asociadas a productos existentes.

Además, el valor de `vr_comision` se determina a partir del campo `comision_admin` definido en `TB_PRODUCTOS_CAT`.

Por ejemplo, si un producto tiene:

```text
cod_prod = CR013
comision_admin = 8

De esta forma, la tabla no genera de manera independiente los valores de comisión, sino que mantiene la relación con el catálogo de productos.

### Tipo de comisión

De acuerdo con la información disponible en `TB_PRODUCTOS_CAT`, se utiliza:

```
COMISION_ADMIN
```

como tipo de comisión.

No se agregaron tipos de comisión ni tarifas que no estén definidas en la información disponible del catálogo.

### Estados del cobro

Los registros se distribuyen entre los siguientes estados:

- `COBRADA`: comisión efectivamente cobrada al cliente.
- `PENDIENTE`: comisión registrada pero aún no cobrada.
- `RECHAZADA`: comisión cuyo cobro fue rechazado.

Las comisiones con estado `COBRADA` son las que posteriormente podrán ser consideradas como ingresos efectivos para el cálculo del CLTV.

### Cobertura temporal

Los registros normales cubren un periodo de 12 meses:

```
2025-08-01 → 2026-07-31
```

Adicionalmente, se incorporaron intencionalmente **20 registros con fechas anteriores al periodo definido**, con el objetivo de probar las validaciones de calidad de datos.

La ejecución presentó como fecha mínima:

```
2025-06-14
```

debido a estas anomalías intencionales.

### Valores nulos controlados

Se incorporaron **4.000 valores nulos** en el campo `tip_comision`.

Esto representa exactamente el **5 % de los 80.000 registros**.

El campo fue seleccionado como campo no crítico para mantener completos los identificadores, fechas, valores monetarios y estados necesarios para los análisis principales.

### Anomalías intencionales

Se incorporaron tres tipos de anomalías para permitir la validación posterior de calidad de datos.

#### 1. Comisiones inconsistentes con el catálogo

Se generaron **20 registros** cuyo `vr_comision` no coincide intencionalmente con el valor `comision_admin` definido para el mismo `cod_prod` en `TB_PRODUCTOS_CAT`.

Esta validación permite comprobar la consistencia entre ambas tablas.

Resultado obtenido:

```
Comisiones inconsistentes con el catálogo:
20
```

#### 2. Fechas fuera de rango

Se generaron **20 registros** con fechas anteriores al periodo histórico esperado.

Resultado obtenido:

```
Comisiones fuera del rango:
20
```

#### 3. Duplicados de negocio

Se generaron **20 registros duplicados** utilizando como criterio los principales atributos de negocio:

```
id_cli
cod_prod
fec_cobro
vr_comision
tip_comision
estado_cobro
```

Resultado obtenido:

```
Duplicados de negocio:
20
```

### Validaciones realizadas

Durante la generación se realizaron validaciones de integridad y calidad:

| Validación | Resultado |
| --------------------------------- | ------ |
| Total de comisiones | 80.000 |
| Clientes inexistentes | 0 |
| Productos inexistentes | 0 |
| Nulos en `tip_comision` | 4.000 |
| Inconsistencias con el catálogo | 20 |
| Duplicados de negocio | 20 |
| Comisiones fuera de rango | 20 |
| Comisiones efectivamente cobradas | 71.979 |

La validación de integridad referencial confirmó que todos los valores de `id_cli` corresponden a clientes existentes y que todos los valores de `cod_prod` corresponden a productos registrados en `TB_PRODUCTOS_CAT`.

### Consistencia de la generación

El script utiliza una semilla fija:

```
SEED = 42
```

Esto permite que las ejecuciones posteriores produzcan los mismos registros y resultados bajo las mismas condiciones.

La consistencia fue comprobada ejecutando el script dos veces y verificando que los primeros registros, las distribuciones y los resultados de las validaciones fueran iguales.

### Relación con las necesidades del negocio

`TB_COMISIONES_LOG` proporciona información necesaria para:

- Identificar los ingresos generados por concepto de comisiones.
- Diferenciar las comisiones efectivamente cobradas de las pendientes o rechazadas.
- Analizar los ingresos por producto y cliente.
- Validar la consistencia de las comisiones frente al catálogo de productos.
- Proporcionar información para el cálculo del Customer Lifetime Value (CLTV).

Para el cálculo del CLTV, únicamente las comisiones con estado `COBRADA` deben considerarse como ingresos efectivos.

La tabla de comisiones se utilizará junto con `TB_OBLIGACIONES` para obtener los ingresos asociados a cada cliente durante los últimos 12 meses calendario.

### Formatos de salida

La tabla se exporta en dos formatos para simular un escenario de ingesta heterogénea:

```
Data/TB_COMISIONES_LOG.csv
Data/TB_COMISIONES_LOG.json
```
## Arquitectura de la solución

## Modelo de datos

## Flujo de procesamiento de datos

## Infraestructura como Código (IaC)

## Conclusiones
