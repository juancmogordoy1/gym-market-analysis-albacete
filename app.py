import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from pathlib import Path

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Análisis del Mercado Fitness — Albacete",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/cartographer.png");
        background-attachment: fixed;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CONSTANTES
# =========================================================
DATA_PATH = Path("data/processed/gym_market_opportunity_albacete_growth.csv")

REQUIRED_COLUMNS = [
    "municipio",
    "poblacion_2025",
    "gyms_google_new",
    "fitness_x10k_new",
    "catchment_pop_25km",
    "real_market_potential",
    "opportunity_score_v2",
    "growth_5y",
    "growth_10y",
    "market_type",
    "lat",
    "lon",
    "fitness_population",
    "fitness_ratio"
]

MARKET_COLORS = {
    "Mercado emergente": [0, 200, 0, 160],
    "Mercado competitivo": [0, 120, 255, 160],
    "Oportunidad latente": [255, 140, 0, 180],
    "Mercado débil": [180, 180, 180, 160]
}

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def format_int(value):
    if pd.isna(value):
        return "0"
    return f"{int(value):,}".replace(",", ".")

def format_float(value, decimals=2):
    if pd.isna(value):
        return "-"
    return f"{value:.{decimals}f}"

def get_market_color(tipo):
    return MARKET_COLORS.get(tipo, [180, 180, 180, 160])

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias en el CSV: {missing}")

    # Normalización básica
    df["municipio"] = df["municipio"].astype(str).str.strip()

    numeric_cols = [
    "poblacion_2025",
    "gyms_google_new",
    "fitness_x10k_new",
    "catchment_pop_25km",
    "real_market_potential",
    "opportunity_score_v2",
    "growth_5y",
    "growth_10y",
    "lat",
    "lon",
    "fitness_population",
    "fitness_ratio"
]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def filter_data(df, market_type, min_population, min_score, min_fitness_population):
    filtered = df.copy()

    if market_type != "Todos":
        filtered = filtered[filtered["market_type"] == market_type]

    filtered = filtered[
        (filtered["poblacion_2025"] >= min_population) &
        (filtered["opportunity_score_v2"] >= min_score) &
        (filtered["fitness_population"] >= min_fitness_population)
    ]

    return filtered

    return filtered
        
def render_market_summary(df):
    st.subheader("Resumen del mercado")

    if df.empty:
        st.warning("No hay datos para mostrar con los filtros actuales.")
        return

    top_city = df.sort_values("opportunity_score_v2", ascending=False).iloc[0]

    col1, col2, col3, col4 = st.columns(4)
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

    if df.empty:
        st.info("No hay municipios que cumplan los filtros.")
        return

    columnas = [
    "municipio",
    "poblacion_2025",
    "fitness_population",
    "fitness_ratio",
    "gyms_google_new",
    "fitness_x10k_new",
    "catchment_pop_25km",
    "opportunity_score_v2",
    "market_type"
]

    df_view = df[columnas].sort_values("opportunity_score_v2", ascending=False).copy()

    st.dataframe(
        df_view.style.format({
            "fitness_population": lambda x: format_int(x),
            "fitness_ratio": "{:.2f}",
            "poblacion_2025": lambda x: format_int(x),
            "gyms_google_new": "{:.0f}",
            "fitness_x10k_new": "{:.2f}",
            "catchment_pop_25km": lambda x: format_int(x),
            "real_market_potential": "{:.2f}",
            "opportunity_score_v2": "{:.2f}",
        }),
        use_container_width=True,
        height=420
    )

    csv = df_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar tabla filtrada en CSV",
        data=csv,
        file_name="municipios_fitness_filtrados.csv",
        mime="text/csv"
    )

def render_municipality_detail(df):
    st.subheader("Detalle de un municipio")

    if df.empty:
        st.info("No hay municipios disponibles con los filtros actuales.")
        return

    municipio_seleccionado = st.selectbox(
        "Selecciona un municipio",
        sorted(df["municipio"].dropna().unique())
    )

    fila = df[df["municipio"] == municipio_seleccionado].iloc[0]

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Población", format_int(fila["poblacion_2025"]))
    c2.metric(
        "Gimnasios detectados",
        int(fila["gyms_google_new"]) if not pd.isna(fila["gyms_google_new"]) else 0
    )
    c3.metric("Fitness x 10k", format_float(fila["fitness_x10k_new"]))
    c4.metric("Opportunity score", format_float(fila["opportunity_score_v2"]))
    c5.metric("Población fitness", format_int(fila["fitness_population"]))

    if not pd.isna(fila["fitness_ratio"]):
        ratio_fitness = f"{fila['fitness_ratio']:.1%}"
    else:
        ratio_fitness = "-"

    c6.metric("Ratio fitness", ratio_fitness)

    st.markdown("### Perspectiva del mercado")

    st.info(
        f"""
**{fila['municipio']}** presenta una oportunidad de mercado con **{format_int(fila['poblacion_2025'])} habitantes**
y **{int(fila['gyms_google_new']) if not pd.isna(fila['gyms_google_new']) else 0} gimnasios detectados**.

La densidad fitness es de **{format_float(fila['fitness_x10k_new'])} gimnasios por cada 10.000 habitantes**,
con una **población accesible de {format_int(fila['catchment_pop_25km'])} personas** en un radio de 25 km.

El municipio está clasificado como **{fila['market_type']}**
con un **opportunity score de {format_float(fila['opportunity_score_v2'])}**.
"""
    )

def render_population_map(map_data):
    st.subheader("Mapa demográfico de municipios")
    st.write("El tamaño del punto representa la población estimada de cada municipio.")

    if map_data.empty:
        st.info("No hay datos geográficos para mostrar.")
        return

    map_plot = map_data.copy()
    map_plot["radius_plot"] = np.sqrt(map_plot["poblacion_2025"].clip(lower=0)) * 28

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_plot,
        get_position='[lon, lat]',
        get_color='[255, 140, 0, 200]',
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
            map_style="dark",
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
    "html": "<b>{municipio}</b><br/>Score: {opportunity_score_v2}<br/>Tipo: {market_type}<br/>Gimnasios: {gyms_google_new}",
    "style": {"backgroundColor": "black", "color": "white"}
}
        )
    )

def render_opportunity_map(map_data):
    st.subheader("Mapa de oportunidades fitness")
    st.write("El tamaño del punto representa el índice de oportunidad y el color indica el tipo de mercado fitness.")

    if map_data.empty:
        st.info("No hay datos geográficos para mostrar.")
        return

    map_plot = map_data.copy()
    map_plot["radius_opportunity"] = np.sqrt(map_plot["opportunity_score_v2"].clip(lower=0)) * 120
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
        map_style="dark",
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
    st.subheader("Oportunidad vs crecimiento demográfico")

    if df.empty:
        st.info("No hay datos para graficar.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    tipos = df["market_type"].dropna().unique()

    for tipo in tipos:
        temp = df[df["market_type"] == tipo]
        ax.scatter(
            temp["growth_5y"],
            temp["opportunity_score_v2"],
            s=np.maximum(temp["poblacion_2025"] / 220, 20),
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

def render_top_table(df, top_n):
    st.subheader(f"Top {top_n} oportunidades de mercado")

    if df.empty:
        st.info("No hay datos para mostrar.")
        return

    top = df[df["poblacion_2025"] > 2000].sort_values(
        "opportunity_score_v2",
        ascending=False
    ).head(top_n)

    st.dataframe(
        top[
            [
                "municipio",
                "poblacion_2025",
                "gyms_google_new",
                "fitness_x10k_new",
                "opportunity_score_v2",
                "market_type"
            ]
        ].style.format({
            "poblacion_2025": lambda x: format_int(x),
            "gyms_google_new": "{:.0f}",
            "fitness_x10k_new": "{:.2f}",
            "opportunity_score_v2": "{:.2f}",
        }),
        use_container_width=True
    )

def render_top_bar_chart(df, top_n):
    st.subheader(f"Ranking Top {top_n} de oportunidades")
    st.write(
        "Este ranking muestra los municipios con mayor oportunidad para abrir nuevos gimnasios "
        "según el score calculado a partir de demanda potencial, oferta actual y crecimiento demográfico."
    )

    if df.empty:
        st.info("No hay datos para graficar.")
        return

    top = df.sort_values("opportunity_score_v2", ascending=False).head(top_n)
    top = top.sort_values("opportunity_score_v2")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top["municipio"], top["opportunity_score_v2"])

    ax.set_xlabel("Índice de oportunidad")
    ax.set_ylabel("Municipio")
    ax.set_title("Municipios con mayor oportunidad fitness")
    ax.grid(axis="x", alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    st.pyplot(fig)

def render_insights(df):
    st.subheader("Insights rápidos")

    if df.empty:
        st.info("No hay insights disponibles con los filtros actuales.")
        return

    top_city = df.sort_values("opportunity_score_v2", ascending=False).iloc[0]
    low_supply = df.sort_values("fitness_x10k_new").iloc[0]
    biggest_market = df.sort_values("catchment_pop_25km", ascending=False).iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success(
            f"**Mayor oportunidad:** {top_city['municipio']} "
            f"con score {top_city['opportunity_score_v2']:.2f}"
        )

    with c2:
        st.warning(
            f"**Menor densidad fitness:** {low_supply['municipio']} "
            f"con {low_supply['fitness_x10k_new']:.2f} gimnasios por 10.000 hab."
        )

    with c3:
        st.info(
            f"**Mayor mercado accesible:** {biggest_market['municipio']} "
            f"con {format_int(biggest_market['catchment_pop_25km'])} personas a 25 km"
        )

# =========================================================
# CARGA DE DATOS
# =========================================================
try:
    df = load_data()    
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

map_data = df.dropna(subset=["lat", "lon"]).copy()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Filtros")

market_type_filter = st.sidebar.selectbox(
    "Tipo de mercado",
    ["Todos"] + sorted(df["market_type"].dropna().unique())
)

min_population = st.sidebar.slider(
    "Población mínima",
    min_value=0,
    max_value=int(df["poblacion_2025"].max()),
    value=2000,
    step=500
)

min_score = st.sidebar.slider(
    "Opportunity score mínimo",
    min_value=0.0,
    max_value=float(df["opportunity_score_v2"].max()),
    value=0.0,
    step=0.1
)
min_fitness_population = st.sidebar.slider(
    "Fitness population mínima",
    min_value=0,
    max_value=int(df["fitness_population"].fillna(0).max()),
    value=0,
    step=500
)

top_n = st.sidebar.slider(
    "Número de municipios en ranking",
    min_value=5,
    max_value=20,
    value=10,
    step=1
)

df_filtered = filter_data(
    df,
    market_type_filter,
    min_population,
    min_score,
    min_fitness_population
)
map_data_filtered = df_filtered.dropna(subset=["lat", "lon"]).copy()

# =========================================================
# TÍTULO
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
# RESUMEN
# =========================================================
render_market_summary(df_filtered)
render_insights(df_filtered)

st.divider()
render_variable_dictionary()

# =========================================================
# TABS PRINCIPALES
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Vista general",
    "Municipios",
    "Mapas",
    "Ranking y gráficos"
])

with tab1:
    render_main_table(df_filtered)

with tab2:    
    render_municipality_detail(df_filtered)

with tab3:
    st.subheader("Análisis geográfico del mercado fitness")
    st.write(
        "Visualización espacial de la población, la oferta actual de gimnasios y las oportunidades de mercado."
    )

    render_population_map(map_data_filtered)
    st.divider()
    render_opportunity_map(map_data_filtered)
    render_map_legend()

with tab4:
    render_growth_vs_opportunity(df_filtered)
    st.divider()
    render_top_table(df_filtered, top_n)
    st.divider()
    render_top_bar_chart(df_filtered, top_n)


    