import altair as alt
import pandas as pd
import streamlit as st
from libaudio import df, jdf
from st_aggrid import AgGrid

st.set_page_config(
    page_title="Farmacodinámica Parkinson", page_icon="⬇", layout="wide"
)

@st.experimental_memo
def get_data():
    source = pd.read_csv('stocks2.csv')
    source = source[source.fecha.gt("2008-01-01")]
    return source

@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolución mediciones pacientes Parkinson")
        .mark_line()
        .encode(
            x="fecha",
            y="nivel",
            color="paciente",
            # strokeDash="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(date)",
            y="nivel",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("fecha", title="Fecha"),
                alt.Tooltip("nivel", title="Nivel Parkinson (UPDRS)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.title("⬇ Farmacodinámica Parkinson")

st.write("registro de medicaciones y mediciones de pacientes")

url2 = 'https://share.streamlit.io/sergiolucero/st2/main/app.py'
html = f'<A HREF="{url2}">Audios Pacientes</A>'
st.components.v1.html(html)

col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input("Elige un paciente (⬇💬👇ℹ️ ...)", value="⬇")
with col2:
    ticker_dx = st.slider("Horizontal offset", min_value=-30, max_value=30, step=1, value=0    )
with col3:
    ticker_dy = st.slider("Vertical offset", min_value=-30, max_value=30, step=1, value=-10    )

# Original time series chart. Omitted `get_chart` for clarity
source = get_data()
chart = get_chart(source)

# Input annotations
ANNOTATIONS = [
    ("Mar 01, 2008", "granxi GOOG"),
    ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
    ("Nov 01, 2008", "Market starts again thanks to..."),
]

# Create a chart with annotations
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["fecha", "evento"])
annotations_df.date = pd.to_datetime(annotations_df.fecha)
annotations_df["y"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=15, text=ticker, dx=ticker_dx, dy=ticker_dy, align="center")
    .encode(
        x="fecha:T",
        y=alt.Y("y:Q"),
        tooltip=["evento"],
    )
    .interactive()
)

st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)
AgGrid(jdf.round(3).sample(5))
