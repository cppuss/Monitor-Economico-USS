#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:09:40 2023

@author: matias.otthgmail.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

st.set_page_config(layout="wide")


st.sidebar.image("ESCUDOUSS_vertical_color.png", use_column_width=True)
st.title('MONITOR ECONÓMICO CPP USS')
st.header('Visualización de series económicas')


data=pd.read_parquet("datos_monitor.parquet")

def fechas_1(grafico):
    grafico.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1A", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    grafico.update_yaxes(rangemode="tozero")


    return grafico

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

def eje_porcentaje_2(grafico):
    grafico.layout.yaxis.tickformat = ',.2%'
    return grafico

def eje_porcentaje_0(grafico):
    grafico.layout.yaxis.tickformat = ',.0%'
    return grafico

def eje_porcentaje(grafico):
    grafico.layout.yaxis.tickformat = ',.1%'
    return grafico

def extremos(data):
    return [data["PERIODO"].iloc[0].to_pydatetime(),data["PERIODO"].iloc[-1].to_pydatetime()]

def gen(imacec_des,rango):
    imacec_des=imacec_des[(imacec_des["PERIODO"]> rango[0])&(imacec_des["PERIODO"]< rango[1])]
    imacec_des = px.line(imacec_des, x="PERIODO", y="VALOR", color="SERIE")
    return imacec_des


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data



tab1, tab2,tab3,tab4 = st.tabs(["ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"])


data1=data[data["CATEGORIA"]=="ACTIVIDAD ECONOMICA"]
data11=data1[data1["CATEGORIA2"]=="IMACEC"]


imacec_des="Imacec empalmado, desestacionalizado (índice 2018=100)"
imacec_des=data11[data11["NOMBRE_2"]==imacec_des]
imacec_des["VALOR"]=imacec_des["VALOR"]/imacec_des["VALOR"].shift(12)-1
imacec_des=imacec_des.dropna()
imacec_des["SERIE"]="Imacec desestacionalizado"

ext_imacec_des=extremos(imacec_des)



imacec_or="Imacec empalmado, serie original (índice 2018=100)"
imacec_or=data11[data11["NOMBRE_2"]==imacec_or]
imacec_or["VALOR"]=imacec_or["VALOR"]/imacec_or["VALOR"].shift(12)-1
imacec_or=imacec_or.dropna()
imacec_or["SERIE"]="Imacec (variación anual)"
data_imacec_or=imacec_or.copy(deep=True)
data_imacec_or=data_imacec_or[["PERIODO","VALOR","SERIE"]]
ext_imacec_or=extremos(imacec_or)


data12=data1[data1["CATEGORIA2"]=="IMACEC - COMPONENTES"]
data12["VALOR"]=data12["VALOR"]/100

est="Indicador mensual de actividad económica, Imacec, contribución porcentual respecto de igual periodo del año anterior, referencia 2018"
est=data12[data12["NOMBRE_1"]==est]
est=est[~(est["NOMBRE_2"]=="Imacec no minero")]
est["SERIE"]=est["NOMBRE_2"]
est=px.line(est, x="PERIODO", y="VALOR", color="SERIE")
est=fechas_2(est)
est=eje_porcentaje(est)


des="Indicador mensual de actividad económica, Imacec, contribución porcentual respecto al periodo anterior, desestacionalizado, referencia 2018"
des=data12[data12["NOMBRE_1"]==des]
des=des[~(des["NOMBRE_2"]=="Imacec no minero")]
des["SERIE"]=des["NOMBRE_2"]
des=px.line(des, x="PERIODO", y="VALOR", color="SERIE")
des=fechas_2(des)
des=eje_porcentaje(des)


data13=data1[data1["CATEGORIA2"]=="PIB"]

per="PIB  per  cápita, referencia 2018  (USD)"
per=data13[data13["NOMBRE_2"]==per]
per["SERIE"]=per["NOMBRE_2"]
per= px.line(per, x="PERIODO", y="VALOR", color="SERIE")
per=fechas_2(per)


nom="PIB, volumen a precios del año anterior encadenado, referencia 2018 (miles de millones de pesos encadenados)"
nom=data13[data13["NOMBRE_2"]==nom]
nom["VALOR"]=nom["VALOR"]/nom["VALOR"].shift(4)-1
nom=nom.dropna()
nom["SERIE"]="PIB Trimestral (variación anual)"
nom= px.line(nom, x="PERIODO", y="VALOR", color="SERIE")
nom=fechas_2(nom)
nom=eje_porcentaje(nom)




with tab1:
    st.write('¡En esta sección se encuentras las variables de crecimiento económico!')

    tab11,tab12,tab13=st.tabs(["IMACEC BRUTO","IMACEC COMPONENTES","CRECIMIENTO ECONÓMICO"])
    
    with tab11:
        st.write('¡Índice Mensual de Actividad Económica! :tractor: ')
        
        appointment = st.slider(
            "Seleccione el rango de fechas",
            value=(ext_imacec_or[0],ext_imacec_or[1]),
            format="YYYY/MM")
        submit1=st.button(label='Generar')
        
        
        if submit1:
            imacec_or=gen(imacec_or,appointment)
            imacec_or=fechas_2(imacec_or)
            imacec_or=eje_porcentaje(imacec_or)
            st.plotly_chart(imacec_or, theme="streamlit", use_container_width=True)
            df_xlsx = to_excel(data_imacec_or)
            st.download_button(label='📥 Download Current Result',
                                            data=df_xlsx ,
                                            file_name= 'df_test.xlsx')

          
            imacec_des=gen(imacec_des,appointment)
            imacec_des=fechas_2(imacec_des)
            imacec_des=eje_porcentaje(imacec_des)
            st.plotly_chart(imacec_des, theme="streamlit", use_container_width=True)
        
    
        with st.expander("Detalle"):
              st.write("""
                  IMACEC: Corresponde a los datos XXX...
                  """)        
                 
    with tab12:
        st.write('¡Índice Mensual de Actividad Económica! :tractor: ')
     
        st.plotly_chart(est, theme="streamlit", use_container_width=True)
        
        st.plotly_chart(des, theme="streamlit", use_container_width=True)
        
    
        
        with st.expander("Detalle"):
            st.write("""
                IMACEC: Corresponde a los datos XXX...
                """)
                
                
                
    with tab13:    
        st.write('¡Producto Interno Bruto!')
        
        st.plotly_chart(per, theme="streamlit", use_container_width=True)
        
        st.plotly_chart(nom, theme="streamlit", use_container_width=True)
        
        
        
        with st.expander("Detalle"):
            st.write("""
                PIB: Corresponde a los datos XXX...
                """) 
            
