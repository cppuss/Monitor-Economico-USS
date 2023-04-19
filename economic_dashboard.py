#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:09:40 2023

@author: matias.otthgmail.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px


st.title('MONITOR ECONÓMICO CPP USS')

path=""
imacec=pd.read_excel("/IMACEC.xlsx").dropna()
imacec=imacec.set_index(imacec.columns.values[0])
imacec.columns=imacec.iloc[0]
imacec=imacec.drop(imacec.index.values[0], axis=0)


df=imacec.reset_index()
df["AÑO"]=df[df.columns.values[0]].apply(str).str[2:4]
df["MES"]=df[df.columns.values[0]].apply(str).str[5:7]
df["FECHA"]=df["AÑO"]+ " - "+ df["MES"]
df=df.set_index(df["FECHA"])
del df["AÑO"],df["MES"],df[df.columns.values[0]],df["FECHA"]
df=imacec.stack()
df=df.reset_index()


df3=px.data.gapminder()

fig = px.line(df[df["Periodo"]=="1.Imacec"], x=df.columns.values[0], y=0, color="Periodo", line_group="Periodo",
        line_shape="spline", render_mode="svg")

fig2 = px.line(df, x=df.columns.values[0], y=0, color="Periodo", line_group="Periodo",
        line_shape="spline", render_mode="svg")

fig.update_xaxes(
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

tab1, tab2,tab3,tab4 = st.tabs(["ACTIVIDAD ECONÓMICA","INFLACIÓN","MERCADO LABORAL","CUENTAS CORRIENTES"])



with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
        
    col1, col2, col3 = st.columns(3)
    
    with col1:
       st.header("A cat")
       st.image("https://static.streamlit.io/examples/cat.jpg")
    
    with col2:
       st.header("A dog")
       st.image("https://static.streamlit.io/examples/dog.jpg")
    
    with col3:
       st.header("An owl")
       st.image("https://static.streamlit.io/examples/owl.jpg")




with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    
    
    
    with st.expander("See explanation"):
        st.write("""
            IMACEC: Corresponde a los datos XXX...
            """)
        
with tab3:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    
    
    
    with st.expander("See explanation"):
        st.write("""
            IMACEC: Corresponde a los datos XXX...
            """)
            
with tab4:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    
    
    
    with st.expander("See explanation"):
        st.write("""
            IMACEC: Corresponde a los datos XXX...
            """)
                
