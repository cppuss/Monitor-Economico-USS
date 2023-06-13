
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


data=pd.read_parquet("datos_monitor.parquet")
import plotly.graph_objects as go
x = [1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50]

# Diccionario de traducción para los números en español
diccionario_numeros = {
    1: 'uno',
    2: 'dos',
    3: 'tres',
    4: 'cuatro',
    5: 'cinco'
}

# Convertir los números del eje x a su versión en español
x_labels = [diccionario_numeros[num] for num in x]

# Crear la figura de Plotly con los ejes en español
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))
fig.update_layout(
    xaxis_title='Eje X',
    yaxis_title='Eje Y',
    xaxis=dict(tickmode='array', tickvals=x, ticktext=x_labels),
    yaxis=dict(tickfont=dict(size=14)),
)

# Usar Streamlit para visualizar el gráfico
st.plotly_chart(fig, use_container_width=True)
