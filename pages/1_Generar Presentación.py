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

def fechas_2(grafico):
    grafico.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3A", step="year", stepmode="backward"),
                dict(count=5, label="5A", step="year", stepmode="backward"),
                dict(count=10, label="10A", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    grafico.update_yaxes(rangemode="tozero")


    return grafico

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
extremos_4=[data4["PERIODO"].iloc[0].to_pydatetime(),datetime.datetime.now()]


options = [ "ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL"]
user_input = st.multiselect(label='Selecciones la serie a utilizar', options=options)

dic_options={"ACTIVIDAD ECONÓMICA":["ACTIVIDAD","COMPONENTES"],
             "INFLACIÓN":["ANUAL","COMPONENTES"],
             "MERCADO LABORAL":["DESOCUPACIÓN","INFORMALIDAD","GÉNERO"]
             }

submit=st.checkbox(label='Seleccionar todas las categorías')
if submit:
    user_input=["ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"]
    


if options[0] in user_input:
    serie=options[0]
    st.subheader(serie)
    user_input_1 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_1 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_1[0],extremos_1[1]),
        format="YYYY/MM")
   # try:
   #     if appointment_1 and user_input_1[0]=="IMACEC":
   #         dataimacec=data1[(data1["PERIODO"]> appointment_1[0])&(data1["PERIODO"]< appointment_1[1])]
   # except:
   #     pass
   # try:        
   #     if appointment_1 and user_input_1[1]=="IMACEC":
   #         dataimacec=data1[(data1["PERIODO"]> appointment_1[0])&(data1["PERIODO"]< appointment_1[1])]
   # except:
   #     pass
    
  #  col1, col2 = st.columns(2)
  #  with col1:
  #      try: 
  #          if appointment_1 :
  #             imacec = px.line(dataimacec[dataimacec["SERIE"]=="1.Imacec"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')            
  #             imacec.write_image("imacec.png")
  #             im="imacec.png"
  #             st.image("imacec.png")
  #             os.remove("imacec.png")
  #      except:
  #          pass
            
  #  with col2:
  #      try: 
  #          if appointment_1:
  #  
  #              componentes_imacec=px.line(dataimacec[dataimacec["CATEGORIA2"]=="IMACEC"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
  #              componentes_imacec.write_image("imacec_des.png")
  #              im="imacec_des.png"
  #              st.image("imacec_des.png")
  #              os.remove("imacec_des.png")
  #      except:
  #          pass
 
        
    
if options[1] in user_input:
    serie=options[1]
    st.subheader(serie)
    user_input_2 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_2 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_2[0],extremos_2[1]),
        format="YYYY/MM/DD")

      
    
if options[2]in user_input:
    serie=options[2]
    st.subheader(serie)
    user_input_3 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
    appointment_3 = st.slider(
        "Seleccione el rango de fechas para la serie " + serie,
        value=(extremos_3[0],extremos_3[1]),
        format="YYYY/MM/DD")


#if options[3] in user_input:
#    serie=options[3]
#    st.subheader(serie)
#    user_input_4 = st.multiselect(label='Selecciones la serie a utilizar', options=dic_options[serie])
#    appointment_4 = st.slider(
#        "Seleccione el rango de fechas para la serie " + serie,
#        value=(extremos_4[0],extremos_4[1]),
#       format="YYYY/MM/DD")
    




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
    
   
    
    try:
        data1=data1[(data1["PERIODO"]> appointment_1[0])&(data1["PERIODO"]< appointment_1[1])]
    except:
        pass
    try:
        data2=data2[(data2["PERIODO"]> appointment_2[0])&(data2["PERIODO"]< appointment_2[1])]
    except:
        pass
    try:
        data3=data3[(data3["PERIODO"]> appointment_3[0])&(data3["PERIODO"]< appointment_3[1])]
    except:
        pass
    try:
        data4=data4[(data4["PERIODO"]> appointment_4[0])&(data4["PERIODO"]< appointment_4[1])]
    except:
        pass
    
    #ACTIVIDAD ECONÓMICA
    def gen(imacec_des,rango,titulo):
        imacec_des=imacec_des[(imacec_des["PERIODO"]>= rango[0])&(imacec_des["PERIODO"]<= rango[1])]
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
    def fechas_2(grafico):
        grafico.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=3, label="3A", step="year", stepmode="backward"),
                    dict(count=5, label="5A", step="year", stepmode="backward"),
                    dict(count=10, label="10A", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        grafico.update_yaxes(rangemode="tozero")
    def eje_porcentaje(grafico):
        grafico.layout.yaxis.tickformat = ',.1%'

        return grafico    
    
#SLIDE 1 ACTIVIAD ECONOMICA
    data11=data1[data1["CATEGORIA2"]=="IMACEC"]    
    imacec_or="Imacec empalmado, serie original (índice 2018=100)"
    imacec_or=data11[data11["NOMBRE_2"]==imacec_or]
    imacec_or["VALOR"]=imacec_or["VALOR"]/imacec_or["VALOR"].shift(12)-1
    imacec_or=imacec_or.dropna()
    imacec_or["SERIE"]="Imacec (variación anual)"
    imacec_or_1=gen(imacec_or,appointment_1,"Variación anual del IMACEC")
    imacec_or_1=fechas_2(imacec_or_1)
    imacec_or_1=eje_porcentaje(imacec_or_1)

    data13=data1[data1["CATEGORIA2"]=="PIB"]
    nom="PIB, volumen a precios del año anterior encadenado, referencia 2018 (miles de millones de pesos encadenados)"
    nom=data13[data13["NOMBRE_2"]==nom]
    nom["VALOR"]=nom["VALOR"]/nom["VALOR"].shift(4)-1
    nom=nom.dropna()
    nom["SERIE"]="PIB Trimestral (variación YoY)"
    nom=gen(nom,appointment_1,"Variación Trimestral PIB YoY")
    nom=fechas_2(nom)
    nom=eje_porcentaje(nom)
    
#SLIDE 2 COMPONENTES
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    imacec = px.line(data1[data1["SERIE"]=="1.Imacec"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
    componentes_imacec=px.line(data1[data1["CATEGORIA2"]=="IMACEC"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white') 
    pib_anual= px.line(data1[data1["SERIE"]=="PIB ANUAL"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
    pib_TRIMESTRAL= px.line(data1[data1["SERIE"].isin(["YoY","Desestacionalizado (Variación Trimestral)"])], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
   
    
    #INFLACIÓN
    
    ipcs=["Variación Mensual", "YoY"]
    ipc_a= px.line(data2[data2["SERIE"]==ipcs[1]], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
    ipc_m= px.line(data2[data2["SERIE"]==ipcs[0]], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
    
 
    #MERCADO LABORAL
    desocupados=px.line(data3[data3["SERIE"]=="Tasa de desocupación"], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
    oc_part=px.line(data3[data3["SERIE"].isin(["Tasa de ocupación","Tasa de participación"])], x="PERIODO", y="VALOR", color="SERIE", template='simple_white')
 

        
    title_1 = st.text_input('Título de la presentación', 'Informe de Actividad Económica')
    submit = st.button(label='GENERAR PRESENTACIÓN')
    
    
    
    if submit and user_input == "":
        st.warning("Selecionar una portada")
    
    elif submit and user_input != "":
        with st.spinner('Generando presentación...'):
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


            #AGREGAR GRAFICOS
            width = Inches(8)
            left = Inches(5)
            top = Inches(1)
            
        
            imacec.write_image("imacec.png")
            im="imacec.png"
            add_image(prs.slides[2], image=im, left=left, width=width, top=top)
            os.remove("imacec.png")


            componentes_imacec.write_image("com_imacec.png")
            com_im="com_imacec.png"
            add_image(prs.slides[3], image=com_im, left=left, width=width, top=top)
            os.remove("com_imacec.png")
    
    
            pib_anual.write_image("pib_a.png")
            pib_aa="pib_a.png"
            add_image(prs.slides[4], image=pib_aa, left=left, width=width, top=top)
            os.remove("pib_a.png")
    
    
            pib_TRIMESTRAL.write_image("pib_t.png")
            pib_t="pib_t.png"
            add_image(prs.slides[5], image=pib_t, left=left, width=width, top=top)
            os.remove("pib_t.png")
    
            ipc_a.write_image("ipc_a.png")
            ipc_aa="ipc_a.png"
            add_image(prs.slides[7], image=ipc_aa, left=left, width=width, top=top)
            os.remove("ipc_a.png")
        
            ipc_m.write_image("ipc_m.png")
            ipc_mm="ipc_m.png"
            add_image(prs.slides[8], image=ipc_mm, left=left, width=width, top=top)
            os.remove("ipc_m.png")
    
            desocupados.write_image("desocupados.png")
            desocupadoss="desocupados.png"
            add_image(prs.slides[10], image=desocupadoss, left=left, width=width, top=top)
            os.remove("desocupados.png")
 
            oc_part.write_image("oc_part.png")
            oc_partt="oc_part.png"
            add_image(prs.slides[11], image=oc_partt, left=left, width=width, top=top)
            os.remove("oc_part.png")
    
            cuentas.write_image("cuentas.png")
            cuentass="cuentas.png"
            add_image(prs.slides[13], image=cuentass, left=left, width=width, top=top)
            os.remove("cuentas.png")
        
            desagregadas.write_image("desagregadas.png")
            desagregadass="desagregadas.png"
            add_image(prs.slides[14], image=desagregadass, left=left, width=width, top=top)
            os.remove("desagregadas.png")
    
            try:       
                user_input_1=pd.DataFrame(user_input_1)
            except:
                pass
            
            try:       
                user_input_2=pd.DataFrame(user_input_2)
            except:
                pass
            try:       
                user_input_3=pd.DataFrame(user_input_3)
            except:
                pass
            try:       
                user_input_4=pd.DataFrame(user_input_4)
            except:
                pass
            

            sacar=[]
            
            try:
                if "IMACEC" not in user_input_1.values:
                    sacar.append(3)
                    sacar.append(4)
                if "CRECIMIENTO ECONÓMICO" not in user_input_1.values:
                    sacar.append(5)
                    sacar.append(6)
            except:
                sacar.append(2)
                sacar.append(5)
                sacar.append(6)
                sacar.append(3)
                sacar.append(4)      
    
            try:
                if "YoY" not in user_input_2.values:
                    sacar.append(8)
                if "MENSUAL" not in user_input_2.values:
                    sacar.append(9)           
            except:
                sacar.append(7) 
                sacar.append(8)           
                sacar.append(9)           
      

            try:
                if "DESOCUPACIÓN" not in user_input_3.values:
                    sacar.append(11)
                if "OCUPACIÓN Y PARTICIPACIÓN" not in user_input_3.values:
                    sacar.append(12)
            except:
                sacar.append(10)
                sacar.append(11)           
                sacar.append(12)           

                
            try:
                if "TOTAL" not in user_input_4.values:
                    sacar.append(14)
                if "DESAGREGADAS" not in user_input_4.values:
                    sacar.append(15)
            except:
                sacar.append(13)  
                sacar.append(14)           
                sacar.append(15)  
              
                
              
            x=1
            for i in sacar:
                xml_slides = prs.slides._sldIdLst  
                slides = list(xml_slides)
                xml_slides.remove(slides[i-x]) 
                x=x+1
                
            
            

            #GENERAR ARCHIVO
            filename = 'presentación_{}_{}.pptx'.format("Economía", today)
            binary_output = BytesIO()
            prs.save(binary_output)
            st.download_button(label='Descargar',
                               data=binary_output.getvalue(),
                               file_name=filename)
else:
    pass





