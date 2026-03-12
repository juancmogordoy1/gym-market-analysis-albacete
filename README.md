🏋️ ANALISIS DE OPORTUNIDADES DE ABRIR UN GYMNASIO EN ALBACETE

Proyecto de Data Science aplicado al análisis de mercado fitness, cuyo objetivo es identificar municipios con potencial para abrir nuevos gimnasios en la provincia de Albacete.

El análisis combina datos demográficos, oferta real de gimnasios, crecimiento poblacional y accesibilidad regional para construir un índice de oportunidad de mercado fitness.

El proyecto incluye análisis exploratorio, ingeniería de variables, visualización geoespacial y una aplicación interactiva desarrollada en Streamlit para explorar oportunidades de mercado.

🎯 OBJETIVO

Identificar municipios donde exista demanda potencial de gimnasios pero baja oferta actual, ayudando a detectar oportunidades de negocio en el sector fitness.

El objetivo no es predecir ventas exactas, sino priorizar municipios con mayor potencial relativo para la apertura de nuevos gimnasios.

🧠 LOGICA DEL ANALISIS

El proyecto construye un índice de oportunidad fitness combinando diferentes variables del mercado:

• población del municipio
• población accesible en un radio de 25 km
• número de gimnasios existentes
• densidad de gimnasios por habitante
• crecimiento demográfico
• estimación de población potencialmente interesada en fitness (fitness_population)
• ratio de penetración fitness (fitness_ratio)

Esta combinación permite identificar municipios donde existe demanda potencial no cubierta por la oferta actual.

📊 DATOS UTILIZADOS

El proyecto integra diferentes fuentes de datos.

Datos demográficos

población por municipio (INE)

crecimiento demográfico

Datos económicos

renta media municipal (IRPF)

Datos de mercado fitness

gimnasios detectados mediante Google Places API

Estos datos se combinan para construir variables analíticas que permitan evaluar el potencial de mercado fitness en cada municipio.

🛠 Técnicas utilizadas

Análisis exploratorio de datos (EDA)

Integración de datos de múltiples fuentes

Feature engineering

Construcción de índices analíticos (scoring)

Segmentación exploratoria de municipios

Análisis geoespacial

Visualización de datos

📂 ESTRUCTURA DEL PROYECTO
data/
 ├─ raw/            # datos originales
 └─ processed/      # datos procesados

notebooks/          # análisis exploratorio y desarrollo

src/                # scripts reutilizables

reports/
 ├─ figures/        # gráficos generados
 └─ outputs/        # mapas interactivos

models/             # resultados analíticos
🖥 APLICACION INTERACTIVA
El proyecto incluye una aplicación desarrollada en Streamlit que permite:

explorar municipios con mayor oportunidad de mercado

filtrar por tamaño de población

filtrar por score de oportunidad

analizar la masa crítica de población interesada en fitness

visualizar oportunidades en mapas interactivos

La aplicación convierte el análisis en una herramienta interactiva para explorar oportunidades de negocio.

🚀 ESTADO DEL PROYECTO

Actualmente el proyecto incluye:

✔ dataset integrado a nivel municipal
✔ integración de datos demográficos y oferta fitness
✔ cálculo de variables de mercado fitness
✔ índice de oportunidad de mercado
✔ análisis geoespacial
✔ visualizaciones analíticas
✔ aplicación interactiva en Streamlit
✔ mapas interactivos de oportunidades

▶️ Cómo ejecutar el proyecto
1️⃣ Clonar el repositorio
git clone https://github.com/juancmogordoy1/gym-market-analysis-albacete.git
2️⃣ Instalar dependencias
pip install -r requirements.txt
3️⃣ Ejecutar la aplicación
streamlit run app.py

📈 VISUALIZACIONES DEL ANALISIS
Oportunidad fitness vs crecimiento demográfico

Este gráfico muestra la relación entre el crecimiento poblacional y la oportunidad de mercado fitness.

Municipios con mayor oportunidad

Ranking de municipios con mayor potencial para abrir nuevos gimnasios.

🗺 Mapa interactivo de oportunidades fitness

El proyecto incluye mapas interactivos que permiten explorar la distribución de gimnasios y las oportunidades de mercado en la provincia de Albacete.

Abrir el mapa:

reports/outputs/mapa_final_oportunidades_fitness_albacete.html

El mapa muestra:

municipios coloreados según opportunity score

top oportunidades de mercado

gimnasios existentes detectados con Google Places

💡 CASO DE USO

El análisis permite detectar municipios donde existe:

suficiente población potencial interesada en fitness

baja oferta actual de gimnasios

crecimiento demográfico positivo

mercado regional accesible

Esto permite identificar ubicaciones con mayor probabilidad de éxito para la apertura de nuevos gimnasios.

🔮 POSIBLES MEJORAS FUTURAS

incorporar estructura de edades

incorporar datos de movilidad o commuting

utilizar datos reales de uso de gimnasios

validar el modelo con aperturas reales de gimnasios

integrar más fuentes de datos económicas

👤 AUTOR

Juan Cruz Mogordoy
Proyecto de Data Science – Análisis de mercado fitness
