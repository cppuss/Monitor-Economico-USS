
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

st.markdown("<h1 style='text-align: center; color: black;'>Pruebas</h1>", unsafe_allow_html=True)



st.write(' ')

data=pd.read_parquet("datos_monitor_1.parquet")
data=data[data["CATEGORIA3"]=="NACIONAL"]
st.dataframe(data)



import xlsxwriter

def descargar_datos(data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    
    
    # Escribir el DataFrame en el archivo Excel
    for i, col in enumerate(data.columns):
        worksheet.write(0, i, col)  # Escribir encabezados
        for j, value in enumerate(data[col]):
            worksheet.write(j + 1, i, value)  # Escribir valores
    
    workbook.close()
    
    
    # Crear un botón de descarga para el archivo Excel
    st.download_button(
        label="Descargar data",
        data=output.getvalue(),
        file_name="datos.xlsx",
        mime="application/vnd.ms-excel"
    )

#a=descargar_datos(data)







