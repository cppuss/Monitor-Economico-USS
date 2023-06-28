
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import time
from pptx import Presentation
from io import BytesIO
from datetime import date
from pptx.dml.color import RGBColor
from pptx.util import Inches
import os
from datetime import datetime
st.markdown("<h1 style='text-align: center; color: black;'>MONITOR ECONÓMICO CPP USS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Fechas de publicación información económica</h2>", unsafe_allow_html=True)


st.write(' ')



st.sidebar.image("ESCUDOUSS_vertical_color.png", use_column_width=True)
#st.image("calendario.png")

import plotly.graph_objects as go
from datetime import datetime
import streamlit as st

# Crear los datos de muestra para el gráfico
x = [
    datetime(2023, 1, 1),
    datetime(2023, 2, 1),
    datetime(2023, 3, 1),
    datetime(2023, 4, 1),
    datetime(2023, 5, 1)
]
y = [10, 20, 30, 40, 50]

# Diccionario de traducción para los meses en español
diccionario_meses = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo'
}

# Convertir las fechas del eje x a su versión en español
x_labels = [f"{diccionario_meses[date.month]} {date.year}" for date in x]

# Crear la figura de Plotly con los ejes en español
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))


# Definir función para formatear las anotaciones
def format_annotation(x, y):
    return f'Fecha: {x}<br>Valor: {y}'

# Agregar interactividad con anotaciones personalizadas
fig.update_traces(
    hovertemplate="%{text}<extra></extra>",
    text=[format_annotation(x_val, y_val) for x_val, y_val in zip(x_labels, y)],
    hoverinfo='text'
)

# Usar Streamlit para visualizar el gráfico
st.plotly_chart(fig, use_container_width=True)
