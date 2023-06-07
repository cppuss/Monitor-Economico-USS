
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


data1=data[data["CATEGORIA"]=="ACTIVIDAD ECONOMICA"]

extremos_1=[data1["PERIODO"].iloc[0].to_pydatetime(),datetime.now()]



appointment = st.slider(
                "Seleccione el rango de fechas",
                value=(extremos_1[0],extremos_1[1]),
                format="YYYY/MM")
