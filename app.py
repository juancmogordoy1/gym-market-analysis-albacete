import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Análisis del Mercado Fitness — Albacete",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/cartographer.png");
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def format_int(value):
    return f"{int(value):,}".replace(",", ".")

def get_market_color(tipo):
    colors = {
        "Mercado emergente": [0, 200, 0, 160],
        "Mercado competitivo": [0, 120, 255, 160],
        "Oportunidad latente": [255, 140, 0, 180],
        "Mercado débil": [180, 180, 180, 160]
    }
    return colors.get(tipo, [180, 180, 180, 160])

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/gym_market_opportunity_albacete_growth.csv")

def render_market_summary(df):
    st.subheader("Resumen del mercado")

    col1, col2, col3, col4 = st.columns(4)
    top_city = df.sort_values("opportunity_score_v2", ascending=False).iloc[0]

    col1.metric("Municipios analizados", len(df))
    col2.metric("Población total", format_int(df["poblacion_2025"].sum()))
    col3.metric("Gimnasios detectados", format_int(df["gyms_google_new"].sum()))
    col4.metric(
        "Mayor oportunidad",
        top_city["municipio"],
        f"Índice {top_city['opportunity_score_v2']:.2f}"
    )

def render_variable_dictionary():
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

def render_main_table(df):
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
    st.dataframe(df_view, use_container_width=True, height=300)

def render_municipality_detail(df):
    st.subheader("Detalle de un municipio")

    municipio_seleccionado = st.selectbox(
        "Selecciona un municipio",
        sorted(df["municipio"].dropna().unique())
    )

    fila = df[df["municipio"] == municipio_seleccionado].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Población", format_int(fila["poblacion_2025"]))
    c2.metric("Gimnasios detectados", int(fila["gyms_google_new"]))
    c3.metric("Fitness x 10k", f"{fila['fitness_x10k_new']:.2f}")
    c4.metric("Opportunity score", f"{fila['opportunity_score_v2']:.2f}")

    st.markdown("### Perspectiva del mercado")

    st.info(
        f"""
**{fila['municipio']}** presenta una oportunidad de mercado con **{format_int(fila['poblacion_2025'])} habitantes**
y **{int(fila['gyms_google_new'])} gimnasios detectados**.

La densidad fitness es de **{fila['fitness_x10k_new']:.2f} gimnasios por cada 10.000 habitantes**,
con una **población accesible de {format_int(fila['catchment_pop_25km'])} personas** en un radio de 25 km.

El municipio está clasificado como **{fila['market_type']}**
con un **opportunity score de {fila['opportunity_score_v2']:.2f}**.
"""
    )

def render_population_map(map_data):
    st.subheader("Mapa 1 — Mapa demográfico de municipios")
    st.write("El tamaño del punto representa la población estimada de cada municipio.")

    map_plot = map_data.copy()
    map_plot["radius_plot"] = np.sqrt(map_plot["poblacion_2025"]) * 28

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_plot,
        get_position='[lon, lat]',
        get_color='[255, 120, 0, 120]',
        get_radius="radius_plot",
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=38.9,
        longitude=-1.9,
        zoom=7
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "text": "{municipio}\nPoblación: {poblacion_2025}\nGimnasios: {gyms_google_new}\nScore: {opportunity_score_v2}"
            }
        )
    )

def render_opportunity_map(map_data):
    st.subheader("Mapa 2 — Mapa de oportunidades fitness")
    st.write("El tamaño del punto representa el índice de oportunidad y el color indica el tipo de mercado fitness.")

    map_plot = map_data.copy()
    map_plot["radius_opportunity"] = np.sqrt(map_plot["opportunity_score_v2"]) * 120
    map_plot["color"] = map_plot["market_type"].apply(get_market_color)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_plot,
        get_position='[lon, lat]',
        get_color="color",
        get_radius="radius_opportunity",
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=38.9,
        longitude=-1.9,
        zoom=7
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "text": "{municipio}\nScore: {opportunity_score_v2}\nTipo: {market_type}\nGimnasios: {gyms_google_new}"
            }
        )
    )

def render_map_legend():
    st.markdown("### Leyenda del mapa")

    st.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
    <div style="width: 18px; height: 18px; background-color: rgb(0,200,0); border-radius: 50%;"></div>
    <div><b>Mercado emergente</b> — alto crecimiento y alta oportunidad</div>
</div>

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
    <div style="width: 18px; height: 18px; background-color: rgb(0,120,255); border-radius: 50%;"></div>
    <div><b>Mercado competitivo</b> — alto crecimiento pero mercado más saturado</div>
</div>

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
    <div style="width: 18px; height: 18px; background-color: rgb(255,165,0); border-radius: 50%;"></div>
    <div><b>Oportunidad latente</b> — oportunidad pero bajo crecimiento</div>
</div>

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
    <div style="width: 18px; height: 18px; background-color: rgb(180,180,180); border-radius: 50%;"></div>
    <div><b>Mercado débil</b> — baja oportunidad y bajo crecimiento</div>
</div>
""", unsafe_allow_html=True)

def render_growth_vs_opportunity(df):
    st.subheader("Gráfico 1 — Oportunidad vs crecimiento demográfico")

    fig, ax = plt.subplots(figsize=(10, 6))
    tipos = df["market_type"].dropna().unique()

    for tipo in tipos:
        temp = df[df["market_type"] == tipo]
        ax.scatter(
            temp["growth_5y"],
            temp["opportunity_score_v2"],
            s=temp["poblacion_2025"] / 220,
            alpha=0.65,
            label=tipo
        )

    ax.set_xlabel("Crecimiento poblacional a 5 años (%)")
    ax.set_ylabel("Índice de oportunidad")
    ax.set_title("Relación entre crecimiento demográfico y oportunidad de mercado", pad=15)
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(title="Tipo de mercado", frameon=False)

    st.pyplot(fig)

def render_top10_table(df):
    st.subheader("Top 10 oportunidades de mercado")

    top10 = df[df["poblacion_2025"] > 2000].sort_values(
        "opportunity_score_v2",
        ascending=False
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

def render_top10_bar_chart(df):
    st.subheader("Gráfico 2 — Top 10 oportunidades para abrir gimnasios")
    st.write(
        "Este ranking muestra los municipios con mayor oportunidad para abrir nuevos gimnasios "
        "según el opportunity score calculado a partir de demanda potencial, oferta actual "
        "y crecimiento demográfico."
    )

    top10 = df.sort_values("opportunity_score_v2", ascending=False).head(10)
    top10 = top10.sort_values("opportunity_score_v2")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(top10["municipio"], top10["opportunity_score_v2"])

    ax.set_xlabel("Índice de oportunidad")
    ax.set_ylabel("Municipio")
    ax.set_title("Municipios con mayor oportunidad fitness")
    ax.grid(axis="x", alpha=0.2)
    ax.invert_yaxis()

    st.pyplot(fig)

# =========================================================
# CARGA DE DATOS
# =========================================================
df = load_data()
map_data = df.dropna(subset=["lat", "lon"]).copy()

# =========================================================
# TÍTULO Y PRESENTACIÓN
# =========================================================
st.title("Análisis de Oportunidades del Mercado Fitness — Albacete")
st.subheader(
    "Panel interactivo para identificar oportunidades de apertura de gimnasios en los municipios de la provincia de Albacete"
)
st.caption(
    "Fuentes de datos: población municipal, gimnasios detectados con Google Places, mercado potencial y crecimiento demográfico"
)

st.divider()

# =========================================================
# RESUMEN GENERAL DEL MERCADO
# =========================================================
render_market_summary(df)

st.divider()

# =========================================================
# DICCIONARIO DE VARIABLES
# =========================================================
render_variable_dictionary()

# =========================================================
# TABLA PRINCIPAL
# =========================================================
render_main_table(df)

st.divider()

# =========================================================
# DETALLE DE MUNICIPIO
# =========================================================
render_municipality_detail(df)

st.divider()

# =========================================================
# BLOQUE GEOGRÁFICO
# =========================================================
st.subheader("Análisis geográfico del mercado fitness")
st.write(
    "Visualización espacial de la población, la oferta actual de gimnasios y las oportunidades de mercado en la provincia de Albacete."
)

st.divider()

# =========================================================
# MAPA 1 — DEMOGRAFÍA MUNICIPAL
# =========================================================
render_population_map(map_data)

st.divider()

# =========================================================
# MAPA 2 — OPORTUNIDAD DE MERCADO
# =========================================================
st.markdown("#### Exploración del mercado por tipo")

filtro_mercado = st.selectbox(
    "Filtrar por tipo de mercado",
    ["Todos"] + sorted(df["market_type"].dropna().unique())
)

map_data_filtered = map_data.copy()

if filtro_mercado != "Todos":
    map_data_filtered = map_data_filtered[
        map_data_filtered["market_type"] == filtro_mercado
    ]

render_opportunity_map(map_data_filtered)

# =========================================================
# LEYENDA DEL MAPA 2
# =========================================================
render_map_legend()

st.divider()

# =========================================================
# GRÁFICO 1 — CRECIMIENTO VS OPORTUNIDAD
# =========================================================
render_growth_vs_opportunity(df)

# =========================================================
# TABLA — TOP 10 OPORTUNIDADES
# =========================================================
render_top10_table(df)

# =========================================================
# GRÁFICO 2 — RANKING DE OPORTUNIDADES
# =========================================================
render_top10_bar_chart(df)