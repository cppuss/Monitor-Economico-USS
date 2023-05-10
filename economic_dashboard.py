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





st.markdown("<h1 style='text-align: center; color: black;'>MONITOR ECONÓMICO CPP USS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Visualización de series económicas </h2>", unsafe_allow_html=True)


st.write(' ')


col1, col2 = st.columns(2)
with col1:
    st.markdown("<h5 style='text-align: center; color: black;'>Esta sección está destinada a generar vistas gráficas de forma automatizada para la visualización y construcción de documentos en el CPP. </h5>", unsafe_allow_html=True)
with col2:
    st.markdown("<h5 style='text-align: center; color: black;'>En la parte superior derecha de los graficos existen múltiples opciones, al inferior existe más información y está la posibildiad de descargar en formato excel. </h5>", unsafe_allow_html=True)


st.write(' ')
st.write(' ')

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

def gen_2(imacec_des,rango,titulo):
    imacec_des=imacec_des[(imacec_des["PERIODO"]> rango[0])&(imacec_des["PERIODO"]< rango[1])]
    
    # rename_dict = {}
    # for i in imacec_des["SERIE"].drop_duplicates():
    #     rename_dict[i]=i
        
    imacec_des = px.line(imacec_des, x="PERIODO", y="VALOR", color="SERIE", line_dash="line_style", title='Mi gráfico de línea', 
              labels={'x': 'Eje X', 'y': 'Eje Y'}, 
              template='plotly_white', 
              width=700, height=600)
              # color_discrete_map=rename_dict)
    
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

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    #writer.save()
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
data_imacec_des=imacec_des.copy(deep=True)
data_imacec_des=data_imacec_des[["PERIODO","VALOR","SERIE"]]



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
data_est=est.copy(deep=True)
data_est=data_est[["PERIODO","VALOR","SERIE"]]
ext_est=extremos(est)



des="Indicador mensual de actividad económica, Imacec, contribución porcentual respecto al periodo anterior, desestacionalizado, referencia 2018"
des=data12[data12["NOMBRE_1"]==des]
des=des[~(des["NOMBRE_2"]=="Imacec no minero")]
des["SERIE"]=des["NOMBRE_2"]
data_des=des.copy(deep=True)
data_des=data_des[["PERIODO","VALOR","SERIE"]]
ext_des=extremos(des)





data13=data1[data1["CATEGORIA2"]=="PIB"]
per="PIB  per  cápita, referencia 2018  (USD)"
per=data13[data13["NOMBRE_2"]==per]
per["SERIE"]=per["NOMBRE_2"]
ext_per=extremos(per)
data_per=per.copy(deep=True)
data_per=data_per[["PERIODO","VALOR","SERIE"]]




nom="PIB, volumen a precios del año anterior encadenado, referencia 2018 (miles de millones de pesos encadenados)"
nom=data13[data13["NOMBRE_2"]==nom]
nom["VALOR"]=nom["VALOR"]/nom["VALOR"].shift(4)-1
nom=nom.dropna()
nom["SERIE"]="PIB Trimestral (variación anual)"
ext_nom=extremos(nom)
data_nom=nom.copy(deep=True)
data_nom=data_nom[["PERIODO","VALOR","SERIE"]]










with tab1:
    st.write('En esta sección se encuentras las variables de actividad económica y crecimiento.')
    
    tab11,tab12,tab13=st.tabs(["IMACEC","COMPONENTES IMACEC","PRODUCTO INTERNO BRUTO"])
    
    with tab11:
        st.write('Índice Mensual de Actividad Económica :tractor: ')
        
        appointment = st.slider(
            "Seleccione el rango de fechas",
            value=(ext_imacec_or[0],ext_imacec_or[1]),
            format="YYYY/MM")
    
        col1, col2 = st.columns(2)
        with col1:
           if appointment:
               imacec_or=gen(imacec_or,appointment,"Imacec")
               imacec_or=fechas_2(imacec_or)
               imacec_or=eje_porcentaje(imacec_or)
             
                
               st.plotly_chart(imacec_or, theme="streamlit", use_container_width=True)
               df_xlsx = to_excel(data_est)
           
                
        with col2:
            if appointment:
          
              imacec_des=gen(imacec_des,appointment,"Imacec desestacionalizado")
              imacec_des=fechas_2(imacec_des)
              imacec_des=eje_porcentaje(imacec_des)
              st.plotly_chart(imacec_des, theme="streamlit", use_container_width=True)
              df_xlsx2 = to_excel(data_des)
              
        
        
        with st.expander("Detalle"):
             st.write("""
                 IMACEC: Corresponde a los datos XXX...
                 """)    
           
    
          
                 
    with tab12:
        st.write('Índice Mensual de Actividad Económica :tractor: ')
    
        
        appointment = st.slider(
            "Seleccione el rango de fechas",
            value=(ext_des[0],ext_des[1]),
            format="YYYY/MM")
    
        col1, col2 = st.columns(2)
        with col1:
           if appointment:
               est=gen(est,appointment,"Componentes Imacec")
               est=fechas_2(est)
               est=eje_porcentaje(est)
               st.plotly_chart(est, theme="streamlit", use_container_width=True)
               df_xlsx = to_excel(data_imacec_or)
              
                
        with col2:
            if appointment:
          
              des=gen(des,appointment,"Componentes Imacec desestacionalizado")
              des=fechas_2(des)
              des=eje_porcentaje(des)
              st.plotly_chart(des, theme="streamlit", use_container_width=True)
              df_xlsx2 = to_excel(data_imacec_des)
             
        
        
        with st.expander("Detalle"):
             st.write("""
                 IMACEC: Corresponde a los datos XXX...
                 """)    
           
    
                
                
                
    with tab13:    
        st.write('Producto Interno Bruto')
      
        
    
        col1, col2 = st.columns(2)
        with col1:
            appointment_1 = st.slider(
                    "Seleccione el rango de fechas (1)",
                    value=(ext_nom[0],ext_nom[1]),
                    format="YYYY/MM")
            
            if appointment_1:
                nom=gen(nom,appointment_1,"PIB Trimestral YoY [USD]")
                nom=fechas_2(nom)
                nom=eje_porcentaje(nom)

                st.plotly_chart(nom, theme="streamlit", use_container_width=True)
                df_xlsx = to_excel(data_nom)
                
        with col2:
            appointment_2 = st.slider(
                     "Seleccione el rango de fechas (2)",
                     value=(ext_per[0],ext_per[1]),
                     format="YYYY")
            
            if appointment_2:
                per=gen(per,appointment_2,"PIB percápita [USD]")
                per=fechas_2(per)
                
                st.plotly_chart(per, theme="streamlit", use_container_width=True)
                
                df_xlsx2 = to_excel(data_per)
               
        with st.expander("Detalle"):
            st.write("""
                PIB: Corresponde a los datos XXX...
                """) 



#INFLACIÓN

data2=data[data["CATEGORIA"]=="INFLACION"]
data2["VALOR"]=data2["VALOR"]/100


men="IPC, IPC sin volátiles e IPC volátiles, variación mensual, información empalmada"
anu="IPC, IPC sin volátiles e IPC volátiles, variación anual, información empalmada"

inf_men=data2[(data2["NOMBRE_1"]==men)&(data2["NOMBRE_2"]=="IPC General")]
inf_men["SERIE"]=inf_men["NOMBRE_2"]
inf_anu=data2[(data2["NOMBRE_1"]==anu)&(data2["NOMBRE_2"]=="IPC General")]
inf_anu["SERIE"]=inf_anu["NOMBRE_2"]

comp_men=data2[(data2["NOMBRE_1"]==men)&~(data2["NOMBRE_2"]=="IPC General")]
comp_men["SERIE"]=comp_men["NOMBRE_2"]
com_anu=data2[(data2["NOMBRE_1"]==anu)&~(data2["NOMBRE_2"]=="IPC General")]
com_anu["SERIE"]=com_anu["NOMBRE_2"]

ext_inf_men=extremos(inf_men)
data_inf_men=inf_men.copy(deep=True)
data_inf_men=data_inf_men[["PERIODO","VALOR","SERIE"]]


ext_inf_anu=extremos(inf_anu)
data_inf_anu=inf_anu.copy(deep=True)
data_inf_anu=data_inf_anu[["PERIODO","VALOR","SERIE"]]


ext_com_inf_men=extremos(comp_men)
data_comp_men=comp_men.copy(deep=True)
data_comp_men=data_comp_men[["PERIODO","VALOR","SERIE"]]


ext_com_inf_anu=extremos(com_anu)
data_com_anu=com_anu.copy(deep=True)
data_com_anu=data_com_anu[["PERIODO","VALOR","SERIE"]]





with tab2:
    st.write('En esta sección se encuentras las distitnas componentes de inflación')
      
    tab21,tab22=st.tabs(["INFLACIÓN ANUAL","INFLACIÓN MENSUAL"])
    
    
    with tab21:
        appointment_1 = st.slider(
                   "Seleccione el rango de fechas",
                   value=(ext_inf_anu[0],ext_inf_anu[1]),
                   format="YYYY/MM")
        
        col1, col2 = st.columns(2)

        with col1:
            
            if appointment_1:
                inf_anu=gen(inf_anu,appointment_1,"Variación porcentual IPC YoY")
                inf_anu=fechas_2(inf_anu)
                inf_anu=eje_porcentaje(inf_anu)

                st.plotly_chart(inf_anu, theme="streamlit", use_container_width=True)
                df_xlsx = to_excel(data_inf_anu)
              
        with col2:
            
            if appointment_1:
                com_anu=gen(com_anu,appointment_1,"Variación porcentual componentes IPC YoY")
                com_anu=fechas_2(com_anu)
                com_anu=eje_porcentaje(com_anu)
                
                st.plotly_chart(com_anu, theme="streamlit", use_container_width=True)
                
                df_xlsx2 = to_excel(data_com_anu)
               
    with tab22:
        appointment_1 = st.slider(
                   "Seleccione el rango de fechas",
                   value=(ext_inf_men[0],ext_inf_men[1]),
                   format="YYYY/MM")
        
        col1, col2 = st.columns(2)
         
        with col1:
            
            if appointment_1:
                inf_men=gen(inf_men,appointment_1,"Variación porcentual IPC mensual")
                inf_men=fechas_2(inf_men)
                inf_men=eje_porcentaje(inf_men)

                st.plotly_chart(inf_men, theme="streamlit", use_container_width=True)
                df_xlsx = to_excel(data_inf_men)
                      
        with col2:
            
            if appointment_1:
                comp_men=gen(comp_men,appointment_1,"Variación porcentual componentes IPC mensual")
                comp_men=fechas_2(comp_men)
                comp_men=eje_porcentaje(comp_men)
                
                st.plotly_chart(comp_men, theme="streamlit", use_container_width=True)
                
                df_xlsx2 = to_excel(data_comp_men)
             
    with st.expander("Detalle"):
        st.write("""
            IPC: Corresponde a los datos XXX...
            """)


data3=data[data["CATEGORIA"]=="MERCADO LABORAL"]
#MERCADO LABORAL











with tab3:
    st.write('En esta sección se encuentra información del mercado laboral')
        
    tab31,tab32,tab33,tab34,tab35=st.tabs(["EMPLEO NACIONAL","EMPLEO POR GENERO","CATEGORÍAS","SERIES ADMINISTRATIVAS","ÍNDICES DE REMUNERACIONES"])
    
    
    with tab31:
        emp_tasas_nac=data3[(data3["CATEGORIA2"]=="EMPLEO - TASAS")&(data3["CATEGORIA3"]=="Nacional")]
        emp_bruto=data3[(data3["CATEGORIA2"]=="EMPLEO - BRUTOS")&(data3["CATEGORIA3"]=="N")]
        emp_bruto["SERIE"]=emp_bruto["NOMBRE_2"]
        emp_bruto["VALOR"]=emp_bruto["VALOR"]*1000
        ext_emp_bruto=extremos(emp_bruto)
        data_emp_bruto=emp_bruto.copy(deep=True)
        data_emp_bruto=data_emp_bruto[["PERIODO","VALOR","SERIE"]]
        
        
        oc=emp_tasas_nac[emp_tasas_nac["NOMBRE_1"]=="Tasa de desocupación Nacional"]
        oc["SERIE"]=oc["NOMBRE_2"]
        oc["VALOR"]=oc["VALOR"]/100

        des=emp_tasas_nac[~(emp_tasas_nac["NOMBRE_1"]=="Tasa de desocupación Nacional")]
        des["SERIE"]=des["NOMBRE_2"]
        des["VALOR"]=des["VALOR"]/100


        
        ext_oc=extremos(oc)
        data_oc=oc.copy(deep=True)
        data_oc=data_oc[["PERIODO","VALOR","SERIE"]]
        
        ext_des=extremos(des)
        data_des=des.copy(deep=True)
        data_des=data_des[["PERIODO","VALOR","SERIE"]]
     
        
        appointment_1 = st.slider(
                    "Seleccione el rango de fechas",
                    value=(ext_oc[0],ext_oc[1]),
                    format="YYYY/MM")
        
        col1, col2 = st.columns(2)
         
        with col1:
            
            if appointment_1:
                oc=gen(oc,appointment_1,"Tasa de desocupación")
                oc=fechas_2(oc)
                oc=eje_porcentaje(oc)
        
                st.plotly_chart(oc, theme="streamlit", use_container_width=True)
                df_xlsx = to_excel(data_oc)
                      
        with col2:
            
            if appointment_1:
                des=gen(des,appointment_1,"Tasas de ocupación y participación")
                des=fechas_2(des)
                des=eje_porcentaje(des)
                
                st.plotly_chart(des, theme="streamlit", use_container_width=True)
                
                df_xlsx2 = to_excel(data_des)
           
        
        emp_bruto=gen(emp_bruto,appointment_1,"Desagregación población en Edad de Trabajar")
        emp_bruto=fechas_2(emp_bruto)

        st.plotly_chart(emp_bruto, theme="streamlit", use_container_width=True)
        
        df_xlsx3 = to_excel(data_emp_bruto)
      
        
        
        informalidad=data3[(data3["CATEGORIA2"]=="INFORMALIDAD")&(data3["NOMBRE_1"]=="Tasa de informalidad (AS)")]
        informalidad["SERIE"]=informalidad["NOMBRE_2"]
        informalidad["VALOR"]=informalidad["VALOR"]/100
        informalidad=informalidad.sort_values(by="PERIODO")
        ext_infor=extremos(informalidad)
        data_infor=informalidad.copy(deep=True)
        data_infor=data_infor[["PERIODO","VALOR","SERIE"]]
        
        
    
        appointment_3 = st.slider(
                    "Seleccione el rango de fechas  ",
                    value=(ext_infor[0],ext_infor[1]),
                    format="YYYY/MM")
        
        
        if appointment_3:
             informalidad=gen(informalidad,appointment_3,"Tasa de Informalidad")
             informalidad=fechas_2(informalidad)
             informalidad=eje_porcentaje(informalidad)
             
             st.plotly_chart(informalidad, theme="streamlit", use_container_width=True)
             
             df_xlsx4 = to_excel(data_infor)
         
    
    with tab32:
       emp_tasas_nac=data3[(data3["CATEGORIA2"]=="EMPLEO - TASAS")&~(data3["CATEGORIA3"]=="Nacional")]
       emp_bruto=data3[(data3["CATEGORIA2"]=="EMPLEO - BRUTOS")&~(data3["CATEGORIA3"]=="N")]
       emp_bruto["SERIE"]=emp_bruto["NOMBRE_2"]
       emp_bruto["VALOR"]=emp_bruto["VALOR"]*1000
       
       
       ext_emp_bruto=extremos(emp_bruto)
       data_emp_bruto=emp_bruto.copy(deep=True)
       data_emp_bruto=data_emp_bruto[["PERIODO","VALOR","SERIE"]]
      
       oc=emp_tasas_nac[emp_tasas_nac["NOMBRE_1"].isin(["Tasa de desocupación H","Tasa de desocupación M"])]
       oc["SERIE"]=oc["NOMBRE_2"]
       oc["VALOR"]=oc["VALOR"]/100
       des=emp_tasas_nac[~emp_tasas_nac["NOMBRE_1"].isin(["Tasa de desocupación H","Tasa de desocupación M"])]
       des["SERIE"]=des["NOMBRE_2"]
       des["VALOR"]=des["VALOR"]/100
       
       ext_oc=extremos(oc)
       data_oc=oc.copy(deep=True)
       data_oc=data_oc[["PERIODO","VALOR","SERIE"]]
       
       ext_des=extremos(des)
       data_des=des.copy(deep=True)
       data_des=data_des[["PERIODO","VALOR","SERIE"]]
    
       
       appointment_1 = st.slider(
                   "Seleccione el rango de fechas ",
                   value=(ext_oc[0],ext_oc[1]),
                   format="YYYY/MM")
       
       col1, col2 = st.columns(2)
        
       with col1:
           
           if appointment_1:
               oc=gen(oc,appointment_1,"Tasas de desocupación")
               oc=fechas_2(oc)
               oc=eje_porcentaje(oc)
       
               st.plotly_chart(oc, theme="streamlit", use_container_width=True)
               df_xlsx = to_excel(data_oc)
                     
       with col2:
           
           if appointment_1:
               des=gen(des,appointment_1,"Tasas de ocupación y participación")
               des=fechas_2(des)
               des=eje_porcentaje(des)
               
               st.plotly_chart(des, theme="streamlit", use_container_width=True)
               
               df_xlsx2 = to_excel(data_des)
       
       options = [
"Población en edad de trabajar",
"Fuerza de Trabajo",
"Ocupados",
"Desocupados",
"Cesantes",
"Buscando Trabajo (1 vez)"
    ]
    
       user_input = st.multiselect(label='Serie a comparar por género', options=options)
       if user_input:
           if len(user_input)==1:
               emp_bruto=data3[(data3["CATEGORIA2"]=="EMPLEO - BRUTOS")&~(data3["CATEGORIA3"]=="N")]
               emp_bruto["SERIE"]=emp_bruto["NOMBRE_2"]
               emp_bruto=emp_bruto[(emp_bruto["NOMBRE_1"].isin([user_input[0]+" H",user_input[0]+" M"]))]
               emp_bruto=gen(emp_bruto,appointment_1,"Comparación por sexo: "+user_input[0])
               emp_bruto=fechas_2(emp_bruto)
        
               st.plotly_chart(emp_bruto, theme="streamlit", use_container_width=True)
               
               df_xlsx3 = to_excel(data_emp_bruto)
           if len(user_input)==2:
               emp_bruto=data3[(data3["CATEGORIA2"]=="EMPLEO - BRUTOS")&~(data3["CATEGORIA3"]=="N")]
               emp_bruto["SERIE"]=emp_bruto["NOMBRE_2"]
               emp_bruto=emp_bruto[(emp_bruto["NOMBRE_1"].isin([user_input[0]+" H",user_input[0]+" M",user_input[1]+" H",user_input[1]+" M"]))]
               emp_bruto=gen(emp_bruto,appointment_1,"Comparación por sexo: "+user_input[0] +" y "+user_input[1])
               emp_bruto=fechas_2(emp_bruto)
         
               st.plotly_chart(emp_bruto, theme="streamlit", use_container_width=True)
                
               df_xlsx3 = to_excel(data_emp_bruto)
        
           if len(user_input)>2:
               emp_bruto=data3[(data3["CATEGORIA2"]=="EMPLEO - BRUTOS")&~(data3["CATEGORIA3"]=="N")]
               emp_bruto["SERIE"]=emp_bruto["NOMBRE_2"]
               series=[]
               for i in np.linspace(0,len(user_input)-1,len(user_input)):
                   i=int(i)
                   hom=user_input[i]+" H"
                   series.append(hom)
                   muj=user_input[i]+" M"
                   series.append(muj)
                       
               emp_bruto=emp_bruto[(emp_bruto["NOMBRE_1"].isin(series))]
               emp_bruto=gen(emp_bruto,appointment_1,"Comparación métricas por sexo")
               emp_bruto=fechas_2(emp_bruto)
         
               st.plotly_chart(emp_bruto, theme="streamlit", use_container_width=True)
                
               df_xlsx3 = to_excel(data_emp_bruto)
             
       informalidad=data3[(data3["CATEGORIA2"]=="INFORMALIDAD")&~(data3["NOMBRE_1"]=="Tasa de informalidad (AS)")]
       informalidad["SERIE"]=informalidad["NOMBRE_2"]
       informalidad["VALOR"]=informalidad["VALOR"]/100
       informalidad=informalidad.sort_values(by="PERIODO")
       ext_infor=extremos(informalidad)
       data_infor=informalidad.copy(deep=True)
       data_infor=data_infor[["PERIODO","VALOR","SERIE"]]
        
        
    
       appointment_3 = st.slider(
                    "Seleccione el rango de fechas   ",
                    value=(ext_infor[0],ext_infor[1]),
                    format="YYYY/MM")
        
        
       if appointment_3:
            informalidad=gen(informalidad,appointment_3,"Tasas de Informalidad")
            informalidad=fechas_2(informalidad)
            informalidad=eje_porcentaje(informalidad)
            
            st.plotly_chart(informalidad, theme="streamlit", use_container_width=True)
            
            df_xlsx4 = to_excel(data_infor)
     
  
    
  
    
    with tab33:
            
        cate_nac=data3[(data3["CATEGORIA2"]=="CATEGORIAS")&(data3["CATEGORIA3"]=="(AS)")]
        cate_nac["SERIE"]=cate_nac["NOMBRE_2"]
        cate_nac=cate_nac.sort_values(by="PERIODO")
        ext_cate_nac=extremos(cate_nac)
        data_cate_nac=cate_nac.copy(deep=True)
        data_cate_nac=data_cate_nac[["PERIODO","VALOR","SERIE"]]
    
        appointment_5 = st.slider(
                     "Seleccione el rango de fechas    ",
                     value=(ext_cate_nac[0],ext_cate_nac[1]),
                     format="YYYY/MM")
        
        if appointment_5:
             cate_nac=gen(cate_nac,appointment_5,"Categorías de ocupados")
             cate_nac=fechas_2(cate_nac)

             
             st.plotly_chart(cate_nac, theme="streamlit", use_container_width=True)
             
             df_xlsx6 = to_excel(data_cate_nac)
        
        
        
        
        cate_sex=data3[(data3["CATEGORIA2"]=="CATEGORIAS")&~(data3["CATEGORIA3"]=="(AS)")]
        cate_sex["SERIE"]=cate_sex["NOMBRE_1"]
        ext_cate_sex=extremos(cate_sex)
        data_cate_sex=cate_sex.copy(deep=True)
        data_cate_sex=data_cate_sex[["PERIODO","VALOR","SERIE"]]
        
        appointment_6 = st.slider(
                     "Seleccione el rango de fechas      ",
                     value=(ext_cate_sex[0],ext_cate_sex[1]),
                     format="YYYY/MM")
       
        
        
        options = [

"Independientes",
"Dependientes",
"Asalariados",
"Sector privado",
"Sector público",
"Trabajo Doméstico"
         ]
  

        user_input = st.multiselect(label='Serie a comparar por género', options=options)
        
        
        
        
        if appointment_6 or user_input:
            if len(user_input)==1:
                cate_sex=data3[(data3["CATEGORIA2"]=="CATEGORIAS")&~(data3["CATEGORIA3"]=="(AS)")]
                cate_sex["SERIE"]=cate_sex["NOMBRE_1"]
              
                cate_sex=cate_sex[(cate_sex["NOMBRE_1"].isin([user_input[0]+" (H)",user_input[0]+" (M)"]))]
                cate_sex=gen(cate_sex,appointment_6,"Comparación ocupados por sexo: "+user_input[0])
                cate_sex=fechas_2(cate_sex)
         
                st.plotly_chart(cate_sex, theme="streamlit", use_container_width=True)
                
                df_xlsx3 = to_excel(data_cate_sex)
                
                
            if len(user_input)==2:
                cate_sex=data3[(data3["CATEGORIA2"]=="CATEGORIAS")&~(data3["CATEGORIA3"]=="(AS)")]
                cate_sex["SERIE"]=cate_sex["NOMBRE_1"]
                cate_sex=cate_sex[(cate_sex["NOMBRE_1"].isin([user_input[0]+" (H)",user_input[0]+" (M)",user_input[1]+" (H)",user_input[1]+" (M)"]))]
                cate_sex=gen(cate_sex,appointment_6,"Comparación ocupados por sexo: "+user_input[0] +" y "+user_input[1])
                cate_sex=fechas_2(cate_sex)
          
                st.plotly_chart(cate_sex, theme="streamlit", use_container_width=True)
                 
                df_xlsx3 = to_excel(data_cate_sex)
      
            if len(user_input)>2:
                cate_sex=data3[(data3["CATEGORIA2"]=="CATEGORIAS")&~(data3["CATEGORIA3"]=="(AS)")]
                cate_sex["SERIE"]=cate_sex["NOMBRE_1"]
                series=[]
                for i in np.linspace(0,len(user_input)-1,len(user_input)):
                    i=int(i)
                    hom=user_input[i]+" (H)"
                    series.append(hom)
                    muj=user_input[i]+" (M)"
                    series.append(muj)
                        
                cate_sex=cate_sex[(cate_sex["NOMBRE_1"].isin(series))]
                cate_sex=gen(cate_sex,appointment_6,"Comparación ocupados por sexo")
                cate_sex=fechas_2(cate_sex)
          
                st.plotly_chart(cate_sex, theme="streamlit", use_container_width=True)
                 
                df_xlsx3 = to_excel(data_cate_sex)
              
             
        
        with tab34:
            series_adm=data3[(data3["CATEGORIA2"]=="SERIES ADMINISTRATIVAS")&(data3["CATEGORIA3"]=="COTIZANTES")]
            series_adm["SERIE"]=series_adm["NOMBRE_1"]
            where=series_adm["NOMBRE_1"].isin(["Cotizantes-INE","Cotizantes-SP"])
            series_adm=series_adm[where]
            series_adm=series_adm.sort_values(by="PERIODO")
    
            ext_series_adm=extremos(series_adm)
            data_series_adm=series_adm.copy(deep=True)
            data_series_adm=data_series_adm[["PERIODO","VALOR","SERIE"]]
        
            appointment_1 = st.slider(
                          "Seleccione el rango de fechas       ",
                          value=(ext_series_adm[0],ext_series_adm[1]),
                          format="YYYY/MM")
            
            sub11 = st.checkbox(label='Incluir límite inferior y superior')
    
            if appointment_1 and not sub11:
                  series_adm=gen(series_adm,appointment_1,"Comparación ENE y SP")
                  series_adm=fechas_2(series_adm)
    
                 
                  st.plotly_chart(series_adm, theme="streamlit", use_container_width=True)
                 
                  df_xlsx6 = to_excel(data_cate_nac)
        
            if appointment_1 and sub11:
                series_adm=data3[(data3["CATEGORIA2"]=="SERIES ADMINISTRATIVAS")&(data3["CATEGORIA3"]=="COTIZANTES")]
                series_adm["SERIE"]=series_adm["NOMBRE_1"]
                series_adm=series_adm.sort_values(by="PERIODO")
                series_adm=gen(series_adm,appointment_1,"Comparación ENE y SP")
                series_adm=fechas_2(series_adm)
       
                
                st.plotly_chart(series_adm, theme="streamlit", use_container_width=True)
                
                df_xlsx8 = to_excel(data_series_adm)
      
            
            series_adm_2=data3[(data3["CATEGORIA2"]=="SERIES ADMINISTRATIVAS")&(data3["CATEGORIA3"]=="VARIACIONES ANUALES")]
            series_adm_2["SERIE"]=series_adm_2["NOMBRE_1"]
            series_adm_2["VALOR"]=series_adm_2["VALOR"]/100
            series_adm_2=series_adm_2.sort_values(by="PERIODO")
     
            ext_series_adm_2=extremos(series_adm_2)
            data_series_adm_2=series_adm_2.copy(deep=True)
            data_series_adm_2=data_series_adm_2[["PERIODO","VALOR","SERIE"]]
            
            
            series_adm_2=gen(series_adm_2,appointment_1,"Variación Anual ENE y SP")
            series_adm_2=fechas_2(series_adm_2)
            series_adm_2=eje_porcentaje(series_adm_2)
           
            st.plotly_chart(series_adm_2, theme="streamlit", use_container_width=True)
           
            df_xlsx9 = to_excel(data_series_adm_2)
        



        with tab35:
            ind_rem_anual=data[(data["CATEGORIA2"]=="INDICES DE REMUNERACIONES")&(data["CATEGORIA3"]=="ANUAL")]

            ind_rem_anual_r=ind_rem_anual[ind_rem_anual["NOMBRE_2"]=="Índice general de remuneraciones nominal "]
            ind_rem_anual_n=ind_rem_anual[ind_rem_anual["NOMBRE_2"]=="Índice general de remuneraciones real"]
            ind_rem_anual_r["SERIE"]="Variación real Y/Y"     
            ind_rem_anual_n["SERIE"]="Variación nominal Y/Y"    
            
            ind_rem_anual_r["VALOR"]=ind_rem_anual_r["VALOR"]/ind_rem_anual_r["VALOR"].shift(1)-1
            ind_rem_anual_r=ind_rem_anual_r.dropna()

            ind_rem_anual_n["VALOR"]=ind_rem_anual_n["VALOR"]/ind_rem_anual_n["VALOR"].shift(1)-1
            ind_rem_anual_n=ind_rem_anual_n.dropna()
            
            ind_rem_anual_n=ind_rem_anual_n.sort_values(by="PERIODO")
            ind_rem_anual_r=ind_rem_anual_r.sort_values(by="PERIODO")
             
              
            ext_ind_rem_anual_n=extremos(ind_rem_anual_n)
            data_ind_rem_anual_n=ind_rem_anual_n.copy(deep=True)
            data_ind_rem_anual_n=data_ind_rem_anual_n[["PERIODO","VALOR","SERIE"]]
            
            ext_ind_rem_anual_n=extremos(ind_rem_anual_r)
            data_ind_rem_anual_r=ind_rem_anual_r.copy(deep=True)
            data_ind_rem_anual_r=data_ind_rem_anual_r[["PERIODO","VALOR","SERIE"]]
           
            
            appointment_41 = st.slider(
                        "Seleccione el rango de fechas   ",
                        value=(ext_ind_rem_anual_n[0],ext_ind_rem_anual_n[1]),
                        format="YYYY/MM")
            
            col1, col2 = st.columns(2)
             
            with col1:
                
                if appointment_41:
                    ind_rem_anual_r=gen(ind_rem_anual_r,appointment_41,"Variación anual Índice de remuneraciones [real] Y/Y ")
                    ind_rem_anual_r=fechas_2(ind_rem_anual_r)
                    ind_rem_anual_r=eje_porcentaje(ind_rem_anual_r)
            
                    st.plotly_chart(ind_rem_anual_r, theme="streamlit", use_container_width=True)
                    df_xlsx = to_excel(data_ind_rem_anual_n)
                          
            with col2:
                
                if appointment_1:
                    ind_rem_anual_n=gen(ind_rem_anual_n,appointment_41,"Variación anual Índice de remuneraciones [nom] Y/Y ")
                    ind_rem_anual_n=fechas_2(ind_rem_anual_n)
                    ind_rem_anual_n=eje_porcentaje(ind_rem_anual_n)
                    
                    st.plotly_chart(ind_rem_anual_n, theme="streamlit", use_container_width=True)
                    
                    df_xlsx2 = to_excel(data_ind_rem_anual_n)
             
            ind_rem_men=data[(data["CATEGORIA2"]=="INDICES DE REMUNERACIONES")&(data["CATEGORIA3"]=="MENSUAL")]

            ind_rem_men_r=ind_rem_men[ind_rem_men["NOMBRE_2"]=="Índice general de remuneraciones nominal "]
            ind_rem_men_n=ind_rem_men[ind_rem_men["NOMBRE_2"]=="Índice general de remuneraciones real"]
            ind_rem_men_r["SERIE"]="Variación real M/M"     
            ind_rem_men_n["SERIE"]="Variación nominal M/M"    
        
            ind_rem_men_r["VALOR"]=ind_rem_men_r["VALOR"]/ind_rem_men_r["VALOR"].shift(1)-1
            ind_rem_men_r=ind_rem_men_r.dropna()
         
            ind_rem_men_n["VALOR"]=ind_rem_men_n["VALOR"]/ind_rem_men_n["VALOR"].shift(1)-1
            ind_rem_men_n=ind_rem_men_n.dropna()
    
        
            ind_rem_men_r=ind_rem_men_r.sort_values(by="PERIODO")
            ind_rem_men_n=ind_rem_men_n.sort_values(by="PERIODO")
          
           
            ext_ind_rem_men_n=extremos(ind_rem_men_n)
            data_ind_rem_men_n=ind_rem_men_n.copy(deep=True)
            data_ind_rem_men_n=data_ind_rem_men_n[["PERIODO","VALOR","SERIE"]]
            
            ext_ind_rem_men_n=extremos(ind_rem_men_r)
            data_ind_rem_men_r=ind_rem_men_r.copy(deep=True)
            data_ind_rem_men_r=data_ind_rem_men_r[["PERIODO","VALOR","SERIE"]]
           
     
            appointment_44 = st.slider(
                        "Seleccione el rango de fechas    ",
                        value=(ext_ind_rem_men_n[0],ext_ind_rem_men_n[1]),
                        format="YYYY/MM")
             
        
      
            col1, col2 = st.columns(2)
             
            with col1:
                
                if appointment_41:
                    ind_rem_men_r=gen(ind_rem_men_r,appointment_44,"Variación mensual Índice de remuneraciones [real] M/M ")
                    ind_rem_men_r=fechas_2(ind_rem_men_r)
                    ind_rem_men_r=eje_porcentaje(ind_rem_men_r)
            
                    st.plotly_chart(ind_rem_men_r, theme="streamlit", use_container_width=True)
                    df_xlsx = to_excel(data_ind_rem_men_n)
                          
            with col2:
                
                if appointment_1:
                    ind_rem_men_n=gen(ind_rem_men_n,appointment_44,"Variación mensual Índice de remuneraciones [nom] M/M ")
                    ind_rem_men_n=fechas_2(ind_rem_men_n)
                    ind_rem_men_n=eje_porcentaje(ind_rem_men_n)
                    
                    st.plotly_chart(ind_rem_men_n, theme="streamlit", use_container_width=True)
                    
                    df_xlsx2 = to_excel(data_ind_rem_men_r)
               
            ind_rem_men=data[(data["CATEGORIA2"]=="INDICES DE REMUNERACIONES")&(data["CATEGORIA3"]=="MENSUAL")]
        
            ind_rem_men_r=ind_rem_men[ind_rem_men["NOMBRE_2"]=="Índice general de remuneraciones nominal "]
            ind_rem_men_n=ind_rem_men[ind_rem_men["NOMBRE_2"]=="Índice general de remuneraciones real"]
            ind_rem_men_r["SERIE"]="Variación real M/M"     
            ind_rem_men_n["SERIE"]="Variación nominal M/M"    
        
            ind_rem_men_r["VALOR"]=ind_rem_men_r["VALOR"]/ind_rem_men_r["VALOR"].shift(12)-1
            ind_rem_men_r=ind_rem_men_r.dropna()
         
            ind_rem_men_n["VALOR"]=ind_rem_men_n["VALOR"]/ind_rem_men_n["VALOR"].shift(12)-1
            ind_rem_men_n=ind_rem_men_n.dropna()
        
        
            ind_rem_men_r=ind_rem_men_r.sort_values(by="PERIODO")
            ind_rem_men_n=ind_rem_men_n.sort_values(by="PERIODO")
          
           
            ext_ind_rem_men_n=extremos(ind_rem_men_n)
            data_ind_rem_men_n=ind_rem_men_n.copy(deep=True)
            data_ind_rem_men_n=data_ind_rem_men_n[["PERIODO","VALOR","SERIE"]]
            
            ext_ind_rem_men_n=extremos(ind_rem_men_r)
            data_ind_rem_men_r=ind_rem_men_r.copy(deep=True)
            data_ind_rem_men_r=data_ind_rem_men_r[["PERIODO","VALOR","SERIE"]]
           
        
            appointment_44 = st.slider(
                        "Seleccione el rango de fechas     ",
                        value=(ext_ind_rem_men_n[0],ext_ind_rem_men_n[1]),
                        format="YYYY/MM")
             
        
        
            col1, col2 = st.columns(2)
             
            with col1:
                
                if appointment_41:
                    ind_rem_men_r=gen(ind_rem_men_r,appointment_44,"Variación mensual Índice de remuneraciones [real] Y/Y ")
                    ind_rem_men_r=fechas_2(ind_rem_men_r)
                    ind_rem_men_r=eje_porcentaje(ind_rem_men_r)
            
                    st.plotly_chart(ind_rem_men_r, theme="streamlit", use_container_width=True)
                    df_xlsx = to_excel(data_ind_rem_men_n)
                          
            with col2:
                
                if appointment_1:
                    ind_rem_men_n=gen(ind_rem_men_n,appointment_44,"Variación mensual Índice de remuneraciones [nom] Y/Y ")
                    ind_rem_men_n=fechas_2(ind_rem_men_n)
                    ind_rem_men_n=eje_porcentaje(ind_rem_men_n)
                    
                    st.plotly_chart(ind_rem_men_n, theme="streamlit", use_container_width=True)
                    
                    df_xlsx2 = to_excel(data_ind_rem_men_r)
              
        



    
#CUENTAS CORRIENTES

data4=data[data["CATEGORIA"]=="CUENTAS CORRIENTES"]
cuentas=data4[(data4["NOMBRE_1"]=="TOTAL")&~(data4["CATEGORIA2"]=="Jurídica")]

cuentas["SERIE"]=cuentas["NOMBRE_1"]

ext_cuentas=extremos(cuentas)
data_cuentas=cuentas.copy(deep=True)
data_cuentas=data_cuentas[["PERIODO","VALOR","SERIE"]]

            

cuentas_2=data4[(data4["NOMBRE_1"]=="TOTAL")&(data4["CATEGORIA2"]=="Jurídica")]
cuentas_2["SERIE"]=cuentas_2["NOMBRE_1"]

ext_cuentas_2=extremos(cuentas_2)
data_cuentas_2=cuentas_2.copy(deep=True)
data_cuentas_2=data_cuentas_2[["PERIODO","VALOR","SERIE"]]


desagregadas=data4[~(data4["NOMBRE_1"]=="TOTAL")&~(data4["CATEGORIA2"]=="Jurídica")]
desagregadas["SERIE"]=desagregadas["NOMBRE_1"]


ext_desagregadas=extremos(desagregadas)
data_desagregadas=desagregadas.copy(deep=True)
data_desagregadas=data_desagregadas[["PERIODO","VALOR","SERIE"]]




desagregadas_2=data4[~(data4["NOMBRE_1"]=="TOTAL")&(data4["CATEGORIA2"]=="Jurídica")]
desagregadas_2["SERIE"]=desagregadas_2["NOMBRE_1"]

ext_desagregadas_2=extremos(desagregadas_2)
data_desagregadas_2=desagregadas_2.copy(deep=True)
data_desagregadas_2=data_desagregadas_2[["PERIODO","VALOR","SERIE"]]





with tab4:
    st.write('En esta sección se encuentra información de cuentas corrientes - datos CMF')
    tab41,tab42=st.tabs(["TOTALES","DESAGREGADAS"])
    with tab41:
        
        appointment_1 = st.slider(
                    "Seleccione el rango de fechas",
                    value=(ext_cuentas[0],ext_cuentas[1]),
                    format="YYYY/MM")

        cuentas=gen(cuentas,appointment_1,"Número de cuentas corrientes - Personas")
        cuentas=fechas_2(cuentas)

        st.plotly_chart(cuentas, theme="streamlit", use_container_width=True)
        
        df_xlsx = to_excel(data_cuentas)
            
        
        
        cuentas_2=gen(cuentas_2,appointment_1,"Número de cuentas corrientes - Empresas")
        cuentas_2=fechas_2(cuentas_2)

        st.plotly_chart(cuentas_2, theme="streamlit", use_container_width=True)
        
        df_xlsx2 = to_excel(data_cuentas_2)
            
        
    

                    
    with tab42:
        appointment_33 = st.slider(
                    "Seleccione el rango de fechas ",
                    value=(ext_desagregadas[0],ext_desagregadas[1]),
                    format="YYYY/MM")
    
        desagregadas=gen(desagregadas,appointment_33,"Número de cuentas corrientes - Personas - Componentes")
        desagregadas=fechas_2(desagregadas)
    
        st.plotly_chart(desagregadas, theme="streamlit", use_container_width=True)
        
        df_xlsx = to_excel(data_desagregadas)
            
        
        
        desagregadas_2=gen(desagregadas_2,appointment_33,"Número de cuentas corrientes - Empresas - Componentes")
        desagregadas_2=fechas_2(desagregadas_2)
    
        st.plotly_chart(desagregadas_2, theme="streamlit", use_container_width=True)
        
        df_xlsx2 = to_excel(data_desagregadas_2)
        
        
        
    with st.expander("Detalle"):
        st.write("""
            CUENTAS CORREINTES - NATURALES Corresponde a los datos XXX...
            CUENTAS CORREINTES - JURIDICAS Corresponde a los datos XXX...
            
            """)
                        
