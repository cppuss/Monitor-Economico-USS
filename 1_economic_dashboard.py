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

st.set_page_config(layout="wide")
st.title('MONITOR ECONÓMICO CPP USS')



# path="/Users/matias.otthgmail.com/Desktop/USS/Monitor Económico/"

data=pd.read_parquet("datafull.parquet")


# "ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"

data1=data[data["CATEGORIA"]=="ACTIVIDAD ECONOMICA"]
data2=data[data["CATEGORIA"]=="INFLACION"]
data3=data[data["CATEGORIA"]=="MERCADO LABORAL"]
data4=data[data["CATEGORIA"]=="CUENTAS CORRIENTES"]


def fechas_1(grafico):
    grafico.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return grafico






tab1, tab2,tab3,tab4 = st.tabs(["ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"])



imacec = px.line(data1[data1["SERIE"]=="1.Imacec"], x="PERIODO", y="VALOR", color="SERIE")
imacec=fechas_1(imacec)

componentes_imacec=px.line(data1[data1["CATEGORIA2"]=="IMACEC"], x="PERIODO", y="VALOR", color="SERIE")
componentes_imacec=fechas_1(componentes_imacec)


pib_anual= px.line(data1[data1["SERIE"]=="PIB ANUAL"], x="PERIODO", y="VALOR", color="SERIE")
pib_anual=fechas_1(pib_anual)

pib_TRIMESTRAL= px.line(data1[data1["SERIE"].isin(["YoY","Desestacionalizado (Variación Trimestral)"])], x="PERIODO", y="VALOR", color="SERIE")
pib_TRIMESTRAL=fechas_1(pib_TRIMESTRAL)


#ACTIVIDAD ECONÓMICA
with tab1:
    st.write('¡En esta sección se encuentras las variables de crecimiento económico! :sunglasses:')

    tab11,tab12=st.tabs(["IMACEC","CRECIMIENTO ECONÓMICO"])
    
    with tab11:
        st.write('¡Índice Mensual de Actividad Económica! :hammer: :tractor: ')
        st.plotly_chart(imacec, theme="streamlit", use_container_width=True)
        st.plotly_chart(componentes_imacec, theme="streamlit", use_container_width=True)
        with st.expander("Detalle"):
            st.write("""
                IMACEC: Corresponde a los datos XXX...
                """)
                
    with tab12:    
        st.write('¡Producto Interno Bruto! :smirk_cat:')
        st.plotly_chart(pib_anual, theme="streamlit", use_container_width=True)
        st.plotly_chart(pib_TRIMESTRAL, theme="streamlit", use_container_width=True)
        with st.expander("Detalle"):
            st.write("""
                PIB: Corresponde a los datos XXX...
                """) 


ipcs=["Variación Mensual", "YoY"]
ipc_a= px.line(data2[data2["SERIE"]==ipcs[1]], x="PERIODO", y="VALOR", color="SERIE")
ipc_a=fechas_1(ipc_a)

ipc_m= px.line(data2[data2["SERIE"]==ipcs[0]], x="PERIODO", y="VALOR", color="SERIE")
ipc_m=fechas_1(ipc_m)



#INFLACIÓN

with tab2:
    st.plotly_chart(ipc_a, theme="streamlit", use_container_width=True)
    st.plotly_chart(ipc_m, theme="streamlit", use_container_width=True)
    
    
    with st.expander("Detalle"):
        st.write("""
            IPC: Corresponde a los datos XXX...
            """)
    
desocupados=px.line(data3[data3["SERIE"]=="Tasa de desocupación"], x="PERIODO", y="VALOR", color="SERIE")
desocupados=fechas_1(desocupados)
oc_part=px.line(data3[data3["SERIE"].isin(["Tasa de ocupación","Tasa de participación"])], x="PERIODO", y="VALOR", color="SERIE")
oc_part=fechas_1(oc_part)      
    
    
    
    
#MERCADO LABORAL
with tab3:
    st.plotly_chart(desocupados, theme="streamlit", use_container_width=True)
    st.plotly_chart(oc_part, theme="streamlit", use_container_width=True)
      

    with st.expander("Detalle"):
        st.write("""
            Tasas de ocupación : Corresponde a los datos XXX...
            Tasas de desocupados : Corresponde a los datos XXX...
            Tasas de participación : Corresponde a los datos XXX...
           
            """)
  
cuentas=px.line(data4[(data4["SERIE"]=="TOTAL")&~(data4["CATEGORIA2"]=="Jurídica")], x="PERIODO", y="VALOR", color="SERIE")
cuentas=fechas_1(cuentas)
            
cuentas_2=px.line(data4[(data4["SERIE"]=="TOTAL")&(data4["CATEGORIA2"]=="Jurídica")], x="PERIODO", y="VALOR", color="SERIE")
cuentas_2=fechas_1(cuentas_2)
            

desagregadas=px.line(data4[~(data4["SERIE"]=="TOTAL")&~(data4["CATEGORIA2"]=="Jurídica")], x="PERIODO", y="VALOR", color="SERIE")
desagregadas=fechas_1(desagregadas)

desagregadas_2=px.line(data4[~(data4["SERIE"]=="TOTAL")&(data4["CATEGORIA2"]=="Jurídica")], x="PERIODO", y="VALOR", color="SERIE")
desagregadas_2=fechas_1(desagregadas_2)

#CUENTAS CORRIENTES
with tab4:
    tab41,tab42=st.tabs(["TOTALES","DESAGREGADAS"])
    with tab41:
        st.plotly_chart(cuentas, theme="streamlit", use_container_width=True)
        st.plotly_chart(cuentas_2, theme="streamlit", use_container_width=True)
     
        with st.expander("Detalle"):
            st.write("""
                CUENTAS CORREINTES - NATURALES Corresponde a los datos XXX...
                CUENTAS CORREINTES - JURIDICAS Corresponde a los datos XXX...
                
                """)
                    
    with tab42:
        st.plotly_chart(desagregadas, theme="streamlit", use_container_width=True)
        st.plotly_chart(desagregadas_2, theme="streamlit", use_container_width=True)
        
        with st.expander("Detalle"):
            st.write("""
                CUENTAS CORREINTES - NATURALES Corresponde a los datos XXX...
                CUENTAS CORREINTES - JURIDICAS Corresponde a los datos XXX...
                
                """)
                        
                  
                    
