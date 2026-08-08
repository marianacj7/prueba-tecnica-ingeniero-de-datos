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

## Arquitectura de la solución

## Modelo de datos

## Flujo de procesamiento de datos

## Infraestructura como Código (IaC)

## Conclusiones
