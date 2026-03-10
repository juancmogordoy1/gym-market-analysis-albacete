# Análisis de oportunidades para abrir gimnasios en Albacete

Proyecto de Data Science para identificar oportunidades de abrir gimnasios en la provincia de Albacete utilizando:

- datos demográficos
- renta municipal
- oferta real de gimnasios
- scoring analítico
- segmentación exploratoria de municipios
- análisis geoespacial
- análisis geoespacial

Proyecto de Data Science orientado a identificar municipios con potencial para abrir nuevos gimnasios en la provincia de Albacete.

El análisis combina datos demográficos, renta municipal, oferta actual de gimnasios, machine learning y visualización geoespacial.

---

## Objetivo

Identificar municipios donde exista **demanda potencial de gimnasios pero baja oferta actual**, ayudando a detectar oportunidades de negocio en el sector fitness.

---
## Lógica del análisis

El proyecto construye un índice de oportunidad combinando:
- población local
- población accesible en un radio de 25 km
- oferta actual de gimnasios
- crecimiento demográfico
- clasificación del tipo de mercado

El objetivo no es predecir ventas exactas, sino priorizar municipios con mayor potencial relativo de apertura.

## Datos utilizados

El proyecto utiliza varias fuentes de datos:

- Datos de población por municipio (INE)
- Datos de renta municipal (IRPF)
- Datos de gimnasios obtenidos mediante Google Places API

---

## Técnicas utilizadas

- Análisis exploratorio de datos
- Feature engineering
- scoring analítico
- segmentación exploratoria de municipios
- análisis geoespacial
- Análisis geoespacial
- Visualización de datos
- machine learning exploratorio (clustering)

---

## Estructura del proyecto
data/ → datos del proyecto
data/raw/ → datos originales
data/processed/ → datos procesados

notebooks/ → análisis exploratorio y modelado

src/ → scripts reutilizables

reports/ → visualizaciones y mapas

models/ → modelos entrenados


---

## Estado del proyecto

Actualmente el proyecto incluye:

- dataset integrado
- feature engineering
- modelo predictivo
- análisis demográfico
- clasificación de mercados
- visualizaciones
- mapas interactivos

## Cómo ejecutar el proyecto

1. Clonar el repositorio

git clone https://github.com/juancmogordoy1/gym-market-analysis-albacete.git

2. Instalar dependencias

pip install -r requirements.txt

3. Abrir los notebooks

notebooks/

4. Ejecutar la app
streamlit run app.py

## Visualizaciones del análisis

### Oportunidad fitness vs crecimiento demográfico

![Opportunity vs Growth](reports/figures/fitness_opportunity_vs_growth.png)

Este gráfico muestra la relación entre crecimiento poblacional y oportunidad de mercado fitness.

---

### Municipios con mayor oportunidad

![Top Opportunities](reports/figures/top_fitness_opportunities.png)

Ranking de municipios con mayor potencial para abrir nuevos gimnasios.

## Mapa interactivo de oportunidades fitness

El proyecto incluye mapas interactivos que permiten explorar la distribución de gimnasios y las oportunidades de mercado en la provincia de Albacete.

Abrir el mapa:

reports/outputs/mapa_final_oportunidades_fitness_albacete.html

Este mapa muestra:

* municipios coloreados según **opportunity score**
* **top oportunidades de mercado**
* **gimnasios existentes detectados con Google Places**
