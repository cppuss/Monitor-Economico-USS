#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 09:08:02 2023

@author: matias.otthgmail.com
"""


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
import datetime 

st.set_page_config(layout="wide")
st.sidebar.image("ESCUDOUSS_vertical_color.png", use_column_width=True)

def add_image(slide, image, left, top, width):
    slide.shapes.add_picture(image, left=left, top=top, width=width)



def eje_porcentaje(grafico):
    grafico.layout.yaxis.tickformat = ',.1%'
    
    return grafico


def gen(imacec_des,rango,titulo):
    imacec_des=imacec_des[(imacec_des["PERIODO"]> rango[0])&(imacec_des["PERIODO"]< rango[1])]
    imacec_des = px.line(imacec_des, x="PERIODO", y="VALOR", color="SERIE" ,title='Mi gráfico de línea', 
              labels={'x': 'Eje X', 'y': 'Eje Y'}, 
              template='plotly_white', 
              width=700, height=600)
    imacec_des.update_layout(title={
        'text': titulo,
        'x':0.5,
         'xanchor': 'center',
         'yanchor': 'top' 
          },legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0.01
        ))
    return imacec_des



st.markdown("<h1 style='text-align: center; color: black;'>MONITOR ECONÓMICO CPP USS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Generar presentación con información económica</h2>", unsafe_allow_html=True)


st.write(' ')

today = date.today()



data=pd.read_parquet("datos_monitor.parquet")


data1=data[data["CATEGORIA"]=="ACTIVIDAD ECONOMICA"]
data2=data[data["CATEGORIA"]=="INFLACION"]
data3=data[data["CATEGORIA"]=="MERCADO LABORAL"]
data4=data[data["CATEGORIA"]=="CUENTAS CORRIENTES"]



extremos_1=[data1["PERIODO"].iloc[0].to_pydatetime(),datetime.datetime.now()]
extremos_2=[data2["PERIODO"].iloc[0].to_pydatetime(),datetime.datetime.now()]
extremos_3=[data3["PERIODO"].iloc[0].to_pydatetime(),datetime.datetime.now()]
#extremos_4=[data4["PERIODO"].iloc[0].to_pydatetime(),datetime.datetime.now()]


options = [ "ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL"]
user_input = st.multiselect(label='Selecciones la serie a utilizar', options=options)

dic_options={"ACTIVIDAD ECONÓMICA":["ACTIVIDAD","COMPONENTES"],
             "INFLACIÓN":["ANUAL"],
             "MERCADO LABORAL":["DESOCUPACIÓN","INFORMALIDAD","REMUNERACIONES"]
             }

submit=st.checkbox(label='Seleccionar todas las categorías')
if submit:
    user_input=["ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL"]
    


if options[0] in user_input:
    serie=options[0]
    st.subheader(serie)
    user_input_1 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])

try:
    appointment_1 = st.slider("Seleccione el rango de fechas para la series. " + serie,
                    value=(extremos_1[0],extremos_1[1]),
                    format="YYYY/MM")
except:
    pass
