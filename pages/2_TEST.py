
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


output = BytesIO()

# Write files to in-memory strings using BytesIO
# See: https://xlsxwriter.readthedocs.io/workbook.html?highlight=BytesIO#constructor
workbook = xlsxwriter.Workbook(output, {'in_memory': True})
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello')
workbook.close()

st.download_button(
    label="Download Excel workbook",
    data=output.getvalue(),
    file_name="workbook.xlsx",
    mime="application/vnd.ms-excel"
)



