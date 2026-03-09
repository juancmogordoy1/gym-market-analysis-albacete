import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gym Market Opportunity Analysis", layout="wide")

# -------------------------
# Carga de datos
# -------------------------
df = pd.read_csv("data/processed/gym_market_opportunity_albacete_growth.csv")

# -------------------------
# Título
# -------------------------
st.title("Gym Market Opportunity Analysis — Albacete")
st.write(
    """
    Aplicación interactiva para analizar oportunidades de abrir gimnasios
    en la provincia de Albacete usando datos demográficos, oferta actual,
    mercado potencial y crecimiento poblacional.
    """
)

# -------------------------
# Métricas rápidas
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Municipios analizados", len(df))
col2.metric("Población total", f"{int(df['poblacion_2025'].sum()):,}".replace(",", "."))
col3.metric("Gimnasios detectados", f"{int(df['gyms_google_new'].sum()):,}".replace(",", "."))
col4.metric(
    "Mayor oportunidad",
    df.sort_values("opportunity_score_v2", ascending=False).iloc[0]["municipio"]
)

st.divider()

# -------------------------
# Diccionario de variables
# -------------------------
with st.expander("Ver explicación de las variables clave"):
    st.markdown("""
**municipio**: nombre del municipio.  
**poblacion_2025**: población actual estimada del municipio.  
**gyms_google**: gimnasios detectados inicialmente con Google Places.  
**gyms_google_new**: gimnasios detectados tras limpieza/mejora de búsqueda.  
**fitness_x10k_new**: gimnasios por cada 10.000 habitantes.  
**catchment_pop_25km**: población accesible en un radio de 25 km.  
**real_market_potential**: indicador del tamaño potencial del mercado fitness.  
**opportunity_score_v2**: score final de oportunidad de negocio.  
**growth_5y**: crecimiento poblacional a 5 años.  
**growth_10y**: crecimiento poblacional a 10 años.  
**market_type**: clasificación del mercado.
    """)

# -------------------------
# Tabla principal limpia
# -------------------------
st.subheader("Tabla principal de municipios")

columnas_principales = [
    "municipio",
    "poblacion_2025",
    "gyms_google_new",
    "fitness_x10k_new",
    "catchment_pop_25km",
    "real_market_potential",
    "opportunity_score_v2",
    "market_type"
]

df_view = df[columnas_principales].sort_values("opportunity_score_v2", ascending=False)
st.dataframe(df_view, use_container_width=True)

st.divider()

# -------------------------
# Selector de municipio
# -------------------------
st.subheader("Detalle de un municipio")

municipio_seleccionado = st.selectbox(
    "Selecciona un municipio",
    sorted(df["municipio"].dropna().unique())
)

fila = df[df["municipio"] == municipio_seleccionado].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Población", f"{int(fila['poblacion_2025']):,}".replace(",", "."))
c2.metric("Gimnasios detectados", int(fila["gyms_google_new"]))
c3.metric("Fitness x 10k", f"{fila['fitness_x10k_new']:.2f}")
c4.metric("Opportunity score", f"{fila['opportunity_score_v2']:.2f}")

st.write("### Interpretación")
st.write(
    f"""
**{fila['municipio']}** tiene una población de **{int(fila['poblacion_2025']):,}** habitantes,
con **{int(fila['gyms_google_new'])}** gimnasios detectados.

Eso equivale a una densidad de **{fila['fitness_x10k_new']:.2f} gimnasios por cada 10.000 habitantes**.

Su población accesible en un radio de 25 km es de **{int(fila['catchment_pop_25km']):,} personas**,
y su indicador de mercado potencial es **{fila['real_market_potential']:.2f}**.

El municipio está clasificado como **{fila['market_type']}**
y su **opportunity score** es **{fila['opportunity_score_v2']:.2f}**.
    """.replace(",", ".")
)

st.divider()

# -------------------------
# Top oportunidades
# -------------------------
st.subheader("Top 10 oportunidades de mercado")

top10 = df[df["poblacion_2025"] > 2000].sort_values(
    "opportunity_score_v2", ascending=False
).head(10)

st.dataframe(
    top10[
        [
            "municipio",
            "poblacion_2025",
            "gyms_google_new",
            "fitness_x10k_new",
            "opportunity_score_v2",
            "market_type"
        ]
    ],
    use_container_width=True
)