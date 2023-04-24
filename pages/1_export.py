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


st.set_page_config(layout="wide")
st.title('MONITOR ECONÓMICO CPP USS')

st.header('Generar presentación con información económica')

today = date.today()

data=pd.read_parquet("datafull.parquet")
data1=data[data["CATEGORIA"]=="ACTIVIDAD ECONOMICA"]
data2=data[data["CATEGORIA"]=="INFLACION"]
data3=data[data["CATEGORIA"]=="MERCADO LABORAL"]
data4=data[data["CATEGORIA"]=="CUENTAS CORRIENTES"]


extremos_1=[data1["PERIODO"].iloc[0].to_pydatetime(),data1["PERIODO"].iloc[-1].to_pydatetime()]
extremos_2=[data2["PERIODO"].iloc[0].to_pydatetime(),data2["PERIODO"].iloc[-1].to_pydatetime()]
extremos_3=[data3["PERIODO"].iloc[0].to_pydatetime(),data3["PERIODO"].iloc[-1].to_pydatetime()]
extremos_4=[data4["PERIODO"].iloc[0].to_pydatetime(),data4["PERIODO"].iloc[-1].to_pydatetime()]


options = [ "ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"]
user_input = st.multiselect(label='Selecciones la serie a utilizar', options=options)

dic_options={"ACTIVIDAD ECONÓMICA":["IMACEC","CRECIMIENTO ECONÓMICO"],
             "INFLACIÓN":["YoY","MENSUAL"],
             "MERCADO LABORAL":["DESOCUPACIÓN","OCUPACIÓN","PARTICIPACIÓN"],
             "CUENTAS CORRIENTES":["TOTAL","DESAGREGADAS"]
             }




if options[0] in user_input:
    serie=options[0]
    st.subheader(serie)
    user_input_1 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_1 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_1[0],extremos_1[1]),
        format="YYYY/MM/DD")
else:
    pass
    
if options[1] in user_input:
    serie=options[1]
    st.subheader(serie)
    user_input_2 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_2 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_2[0],extremos_2[1]),
        format="YYYY/MM/DD")
else:
    pass
      
    
if options[2]in user_input:
    serie=options[2]
    st.subheader(serie)
    user_input_3 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_3 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_3[0],extremos_3[1]),
        format="YYYY/MM/DD")
else:
    pass

if options[3] in user_input:
    serie=options[3]
    st.subheader(serie)
    user_input_4 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_4 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_4[0],extremos_4[1]),
        format="YYYY/MM/DD")
else:
    pass    
    


    
#submit = st.checkbox(label='RESUMEN')

#if submit:     
#    inputs=pd.DataFrame()
#    try:    
#        inputs=inputs.append(user_input)
#    except:
#        pass    
#    try:    
#        inputs=inputs.append(user_input_2)
#    except:
#        pass    
#    try:    
#        inputs=inputs.append(user_input_3)
#    except:
#        pass    
#    try:    
#        inputs=inputs.append(user_input_4)
#    except:
#        pass    
#    st.table(inputs)



sub1 = st.checkbox(label='Exportar como presentación')

if sub1:
    
    genre = st.radio(
        "Seleccionar un formato",
        ('Formato claro', 'Formato oscuro'))

    
    col1, col2 = st.columns(2)
    with col1:
       st.subheader("Formato claro")
       st.image("OPCION1.png")
       
    with col2:
       st.subheader("Formato oscuro")
       st.image("OPCION2.png")
    
    title_1 = st.text_input('Título de la presentación', 'Informe de Actividad Económica')
    submit = st.button(label='GENERAR PRESENTACIÓN')
    

    
    if submit and user_input == "":
        st.warning("Selecionar una portada")
    
    elif submit and user_input != "":
        with st.spinner('Generating awesome slides for you...'):
            prs=Presentation("BASE PRESENTACION USS_STGO-BES.pptx")
            xml_slides = prs.slides._sldIdLst  
            slides = list(xml_slides)
            
            if genre=="Formato claro" :           
                xml_slides.remove(slides[1]) 
            else: 
                xml_slides.remove(slides[0]) 
            
            #GENERAR PRESENTACIÓN
            slide = prs.slides[0]
            title =  slide.shapes.title.text_frame.paragraphs[0]
            title.text = title_1
            title.font.color.rgb = RGBColor(255, 255, 255)  # Color blanco
            title.font.bold = True  # Negrita



            #GENERAR ARCHIVO
            filename = 'presentación.pptx'.format("Economía", today)
            binary_output = BytesIO()
            prs.save(binary_output)
            st.download_button(label='Presiona para descargar',
                               data=binary_output.getvalue(),
                               file_name=filename)
else:
    pass





