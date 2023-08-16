
import streamlit 
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

streamlit.markdown("<h1 style='text-align: center; color: black;'>Pruebas</h1>", unsafe_allow_html=True)



streamlit.write(' ')

data=pd.read_parquet("datos_monitor_1.parquet")
data=data[data["CATEGORIA3"]=="NACIONAL"]
streamlit.dataframe(data)



from streamlit_extras.switch_page_button import switch_page

want_to_contribute = streamlit.button("I want to contribute!")
if want_to_contribute:
    switch_page("1_generar presentacion")



