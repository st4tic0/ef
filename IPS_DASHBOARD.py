# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 16:58:25 2021

@author: IPSMX-GX34G63
"""
# Data load Package
import io

# Core Packages
import streamlit as st
from PIL import Image

# EDA Packages
import pandas as pd
import numpy as np

# Data Viz Packages
import matplotlib
from plotly.subplots import make_subplots
matplotlib.use('Agg')
import plotly.express as px
import plotly.graph_objs as go
#import matplotlib.pyplot as plt
#import seaborn as sns

# ML
# from sklearn.linear_model import LinearRegression

######################################################################################################

APP_TITLE = "IPS Dashboard"
img=Image.open('Imagenes\IPS.png')
st.set_page_config(
    page_title = APP_TITLE,
    page_icon = img,
    layout = "wide")

img_sidebar= st.sidebar.columns(3)
img_sidebar[1].image(img,width=100)

title_1 = st.columns(3)
title_1[1].markdown("<h1 style='text-align: center; color: #132847;'> <br> <b>Production Data Statistics</b></h1> <br>", unsafe_allow_html=True)

######################################################################################################

# funcion Load data

@st.cache
def load_production_data(uploadedfile):
    if uploadedfile:
        string = uploadedfile.read()
        production_data = pd.read_csv(io.StringIO(string.decode('utf-8')))
        production_data = production_data.loc[:, ~production_data.columns.str.contains('^Unnamed')]
        production_data.columns = [x.lower() for x in production_data.columns]
        production_data['fecha'] = pd.to_datetime(production_data['fecha'])
        production_data['lat'] = production_data['lat'].astype(float)
        production_data['lon'] = production_data['lon'].astype(float)
        
    else:
            production_data = None
    
    return production_data

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float

######################################################################################################

def load_pressure_data(uploadedfile_1):
    if uploadedfile_1:
        string = uploadedfile_1.read()
        pressure_data = pd.read_csv(io.StringIO(string.decode('utf-8')))
        pressure_data = pressure_data.loc[:, ~pressure_data.columns.str.contains('^Unnamed')]
        pressure_data.columns = [x.lower() for x in pressure_data.columns]
        pressure_data['fecha'] = pd.to_datetime(pressure_data['fecha'])

    else:
            pressure_data = None
    
    return pressure_data

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float

######################################################################################################

def load_mapa_coords(uploadedfile_2):
    if uploadedfile_2:
        string = uploadedfile_2.read()
        coords = pd.read_csv(io.StringIO(string.decode('utf-8')))
        coords = coords.rename(columns={'LATITUD': 'lat', 'LONGITUD': 'lon'})
        coords = coords.loc[:, ~coords.columns.str.contains('^Unnamed')]
        coords.columns = [x.lower() for x in coords.columns]
        coords = coords.dropna(subset=['lon', 'lat'])

    else:
            coords = None
    
    return coords

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float

######################################################################################################

def load_salt_data(uploadedfile_3):
    if uploadedfile_3:
        string = uploadedfile_3.read()
        salt = pd.read_csv(io.StringIO(string.decode('utf-8')))
        salt = salt.loc[:, ~salt.columns.str.contains('^Unnamed')]
        salt.columns = [x.lower() for x in salt.columns]
        salt = salt.fillna(0)
        salt = salt.rename(columns={"dens.": "densidad", "dens. m": "densidad_m"})
        salt = salt.rename(columns={'pozo': 'terminacion', 'agua': 'water_cut'})
        salt["salinidad"] = salt["salinidad"].astype('str')
        salt['salinidad'] = salt['salinidad'].str.replace(',','')
        salt['salinidad'] = salt['salinidad'].astype(float)
        salt = salt[salt.salinidad >= 1]
        salt = salt[salt.water_cut >= 1]

    else:
            salt = None
    
    return salt

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float

######################################################################################################

# SIDEBAR 0

with st.sidebar.expander('Load Data'):
    uploadedfile = st.file_uploader('Production Data', type=['csv'], key=('Production'))
    production = load_production_data(uploadedfile)
    
    uploadedfile1 = st.file_uploader('Pressure Data', type=['csv'], key=('Pressure'))
    pressure = load_pressure_data(uploadedfile1)
    
    uploadedfile2 = st.file_uploader('Coordinates', type=['csv'], key=('Maps'))
    coords = load_mapa_coords(uploadedfile2)

    uploadedfile3 = st.file_uploader('Salinity', type=['csv'], key=('salt'))
    salt = load_salt_data(uploadedfile3)
    
######################################################################################################

#data = pd.merge(production, pressure, how='outer', on=['terminacion', 'fecha', 'campo'])
#data = data.sort_values(by='terminacion')
#data['fecha'] = data['fecha'] = pd.to_datetime(data['fecha'])

######################################################################################################

# SIDEBAR 1

with st.sidebar.expander('Well Selector'):
    campo = production['campo'].unique()
    camp = st.selectbox('Select an oilfield', campo)
    
    filtrado = production[production['campo'] == camp]
    
    wells = filtrado['terminacion'].unique()
    well = st.selectbox('Select a well', wells)
    
    data1 = filtrado[filtrado['terminacion'] == well]
    
    MM = 1000000

# SIDEBAR 2

with st.sidebar.expander('Declination Curve Analytics'):
    #di = st.sidebar.slider('Di value',0.0, 1.0, (0.130),0.005)
    di = st.number_input('Declination Index Value: ')
    capex = st.number_input('Enter a CAPEX value')
    opening = st.checkbox('CAPEX Reopen Well')
    interval = st.checkbox('CAPEX New Interval')
    reentry= st.checkbox('CAPEX Re-entry')

######################################################################################################

# DATA CHECKING

with st.expander('Raw Data'):
    st.write(production)
    st.write(pressure)
    st.write(coords)
    st.write(salt)

######################################################################################################

# ALL VARIABLES

######################################################################################################

# GOR

# WOR

######################################################################################################

#MAPA Y TABLA
for_map = data1.copy()
for_map = for_map[['campo', 'terminacion', 'fecha', 'class', 'lon', 'lat', 'aceite', 'gas', 'agua', 'aceite_bpd', 'agua_bpd', 'gas_mmcfpd', 'water_cut']]
for_map['fecha'] = for_map['fecha'].dt.date
map_filt = for_map.dropna()
map_filt['fecha'] = pd.to_datetime(map_filt['fecha'], dayfirst=True).dt.strftime('%m-%Y')

# BARRAS Y PIE
oilwells = production.groupby(['terminacion']).sum()
oilwells = oilwells.sort_values(by=['aceite_barrels'])
oilwells = oilwells.nlargest(25, 'aceite_barrels').reset_index()

oilfields = production.groupby(['campo']).sum()
oilfields = oilfields.sort_values(by=['aceite_barrels'])
oilfields = oilfields.nlargest(15, 'aceite_barrels').reset_index()

gaswells = production.groupby(['terminacion']).sum()
gaswells = gaswells.sort_values(by=['gas'])
gaswells = gaswells.nlargest(25, 'gas').reset_index()

gasfields = production.groupby(['campo']).sum()
gasfields = gasfields.sort_values(by=['gas_mmcfpd'])
gasfields = gasfields.nlargest(15, 'gas_mmcfpd').reset_index()

waterwells = production.groupby(['terminacion']).sum()
waterwells = waterwells.sort_values(by=['agua'])
waterwells = waterwells.nlargest(25, 'agua').reset_index()

waterfields = production.groupby(['campo']).sum()
waterfields = waterfields.sort_values(by=['agua_bpd'])
waterfields = waterfields.nlargest(15, 'agua_bpd').reset_index()

# SUBDATA 1 
r = pd.date_range(start=min(data1.fecha), end = max(data1.fecha), freq='M')
start= min(str(data1.fecha))
data1.index = pd.DatetimeIndex(data1.fecha)
data1 =data1.reindex(r, fill_value=0)
data1['fecha'] = data1.index
data1['Mo'] = np.arange(len(data1)) + 1
data1['Yr'] = data1['Mo'] / 12

f = pd.date_range(start='11/30/2021', end='12/31/2031', freq='M')

datad = np.random.randint(1, high=100, size=len(f))

data2 = pd.DataFrame({'fecha': f, 'col2': datad})
data2 = data2.set_index('fecha')
data2['Mo'] = np.arange(len(data2)) + 1
data2['Yr'] = data2['Mo'] / 12
del data2['col2']

cum_pozo = (data1['aceite_bpd'].sum() * 30.5)/MM
cum_gas = (data1['gas_mmcfpd'].sum()*30.5)/MM
cum_agua = (data1['agua_bpd'].sum()*30.5)/MM

data1['Historical trend'] = max(data1['aceite_bpd']) / (1 + 0.000000001 * di * data1['Yr']) ** (1 /0.000000001)
data2['Open'] = 100 / (1 + 0.000000001 * di * data2['Yr']) ** (1 /0.000000001)
data2['Open_Interval'] = 202 / (1 + 0.000000001 * di * data2['Yr']) ** (1 /0.000000001)
data2['Reentry'] = 607 / (1 + 0.000000001 * di * data2['Yr']) ** (1 /0.000000001)

data2['Open'] = np.where(data2['Open']<= 10 , np.nan, data2['Open'])
data2['Open_Interval'] = np.where(data2['Open_Interval']<= 10 , np.nan, data2['Open_Interval'])
data2['Reentry'] = np.where(data2['Reentry']<= 10 , np.nan, data2['Reentry'])

data2['Day'] = data2.index.day
data2['Month'] = data2.index.month
data2['Year'] = data2.index.year

data3 = data2
data4 = data2

data3['Day'] = data2.index.day
data3['Month'] = data2.index.month
data3['Year'] = data2.index.year
data4['Day'] = data2.index.day
data4['Month'] = data2.index.month
data4['Year'] = data2.index.year
data2['Price'] = 60
data2['Open_monthly'] = data2['Open'] * data2['Day']
data2['Open_Interval_monthly'] = data2['Open_Interval'] * data2['Day']
data2['Reentry_monthly'] = data2['Reentry'] * data2['Day']
data2['Revenue_Open'] = 60 * data2['Open'] * data2['Day']
data2['Revenue_Open_Interval'] = 60 * data2['Open_Interval'] * data2['Day'] 
data2['Revenue_Reentry'] = 60 * data2['Reentry'] * data2['Day']

data3= data2.groupby(["Year",'Month'], as_index=False)['Open_monthly','Revenue_Open'].sum()

data4= data2.groupby(["Year",'Month'], as_index=False)['Open_Interval_monthly','Revenue_Open_Interval'].sum()

data5= data2.groupby(["Year",'Month'], as_index=False)['Reentry_monthly','Revenue_Reentry'].sum()

#del filtrado['water_cut']
filtrado.index = pd.DatetimeIndex(filtrado.fecha)
filtrado['Aceite_Anual'] = filtrado['aceite_bpd'] * filtrado['dias']
filtrado['Gas_Anual'] = filtrado['gas'] * filtrado['dias']
filtrado['Agua_Anual'] = filtrado['agua_bpd'] * filtrado['dias']
filtrado['Day'] = filtrado.index.day
filtrado['Month'] = filtrado.index.month
filtrado['Year'] = filtrado.index.year
    
      
fil= filtrado.groupby(["Year"], as_index=False)['Aceite_Anual','Gas_Anual','Agua_Anual'].sum()
fil['water_cut1'] = fil['Agua_Anual'] / (fil['Agua_Anual']+fil['Aceite_Anual'])

cum_pozo_camp = (fil['Aceite_Anual'].sum())/MM
cum_gas_camp = (fil['Gas_Anual'].sum())/MM
cum_agua_camp = (fil['Agua_Anual'].sum())/MM

######################################################################################################

#Press variables

filtrado_press = pressure[pressure['campo'] == camp]
filtrado_press.index = pd.DatetimeIndex(filtrado_press.fecha)
filtrado_press['Day'] = filtrado_press.index.day
filtrado_press['Month'] = filtrado_press.index.month
filtrado_press['Year'] = filtrado_press.index.year

fil2= filtrado_press.groupby(["Year"], as_index=False)['cerrado(yac)', 'cerrado(pozo)', 'fluyendo(yac)', 'fluyendo(pozo)'].sum()
#'cerrado(yac)', 'cerrado(pozo)', 'fluyendo(yac)', 'fluyendo(pozo)'#

######################################################################################################



######################################################################################################

# FIGURAS
with st.expander('Production Data'):
    #st.map(coords)
    #FILA 1
    # FIG 1 - MAPA
    map_all_data = px.scatter_mapbox(coords, lat="lat", lon="lon", hover_name="terminacion", zoom=8, color='campo')
    map_all_data.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, height=600, width=1000)
    #map_all_data.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    st.plotly_chart(map_all_data)
    
    cols2 = st.columns(2)

    # FIG 2 - PRODUCCION HISTORICA DEL CAMPO
    st.subheader(f"{camp} Historical Production: ")
    field_prod = make_subplots(specs=[[{"secondary_y": True}]])

    field_prod.add_trace(go.Scatter(x=fil['Year'],y=fil['Aceite_Anual'], mode='lines+markers', marker_symbol = 'diamond', marker_line_width=.5, marker=dict(size=4,color='#8FC93A'),name='Oil'), secondary_y=False)
    field_prod.add_trace(go.Scatter(x=fil['Year'],y=fil['Agua_Anual'], mode='lines+markers', marker_line_width=.5, marker=dict(size=4,color='dodgerblue'), name='Water'), secondary_y=False)
    field_prod.add_trace(go.Scatter(x=fil['Year'],y=fil['Gas_Anual'],mode='lines+markers', marker_symbol = 'triangle-up', marker_line_width=.5,marker=dict(size=4,color='#DD1C1A'),name='Gas'), secondary_y=True)
    
    # Set x-axis title
    field_prod.update_layout(title=f'<b>Oilfield Historical Production - {camp}</b>', hovermode="x unified")
    field_prod.update_xaxes(title_text="<b>Year</b>")
    field_prod.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=500)
    # Set y-axes titles
    #field_prod.update_layout(yaxis1=dict(type='log'))
    # update
    field_prod.update_yaxes(title_text="<b>Oil [bbl/d] / Water Production [bbl/d]</b> ", secondary_y=False)
    field_prod.update_yaxes(title_text="<b>Gas Production Rate [Cubic Meters per Day] </b>", secondary_y=True)
    field_prod.update_yaxes(nticks=25,secondary_y=False)
    field_prod.update_yaxes(nticks=25,secondary_y=True)
    field_prod.update_xaxes(nticks=10)
    
    st.subheader(f"{camp} Historical Production: ")
    st.caption("Cum Oil: " + str(round(cum_pozo_camp,2)) + " MMBO")
    st.caption("Cum Gas: " + str(round(cum_gas_camp,2)) + " MMCFPD")
    st.caption("Cum Water: " + str(round(cum_agua_camp,2)) + " MMBO")
    
    cols2[0].plotly_chart(field_prod)
    
    field_press = make_subplots(specs=[[{"secondary_y": False}]])

    field_press.add_trace(go.Scatter(x=fil2['Year'],y=fil2['cerrado(yac)'], mode='lines', line={'dash': 'dash', 'color': 'black'}, name='Reservoir<br>Pressure<br>(plugged)'))
    field_press.add_trace(go.Scatter(x=fil2['Year'],y=fil2['cerrado(pozo)'], mode='lines', line={'dash': 'dash', 'color': 'red'}, name='Well<br>Pressure<br>(plugged)'))
    field_press.add_trace(go.Scatter(x=fil2['Year'],y=fil2['fluyendo(yac)'], mode='lines', line={'color': 'black'}, name='Reservoir<br>Pressure<br>(open)'))
    field_press.add_trace(go.Scatter(x=fil2['Year'],y=fil2['fluyendo(pozo)'], mode='lines', line={'color': 'red'}, name='Well<br>Pressure<br>(open)'))
    
    # Set x-axis title
    field_press.update_layout(title=f'<b>Oilfield Historical Pressure - {camp}</b>', hovermode="x unified")
    field_press.update_xaxes(title_text="<b>Year</b>")
    field_press.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=500)
    # Set y-axes titles
    field_press.update_layout(yaxis1=dict(type='log'))
    # update
    field_press.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b> ", secondary_y=False)
    field_press.update_yaxes(nticks=10,secondary_y=True)
    field_press.update_xaxes(nticks=50)
    
    cols2[1].plotly_chart(field_press)
    
    ####NOTES####   
    
    #FILA 2
    cols3 = st.columns(2)
    
    # FIG 3 - PRODUCCION HISTORICA POR PARTES/TODOS LOS POZOS
    
    ##OIL##
    oil = px.scatter(filtrado, x= filtrado.index, y="aceite_bpd", log_y=False, color="terminacion")
        
    # update layout
    oil.update_layout(title=f'<b>Oil Production - {camp}</b>')
    #oil.update_layout(hovermode="x unified")
    #oil.update_layout(yaxis1=dict(type='log'))
    
    # update trace
    oil.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update axis
    oil.update_yaxes(title_text="<b>Oil (BOPD)</b>", nticks=10)
    oil.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols3[0].plotly_chart(oil)
    
    ##GAS##
    gas = px.scatter(filtrado, x= filtrado.index, y="gas", log_y=False, color="terminacion")
    
    # update layout
    gas.update_layout(title=f'<b>Gas Production - {camp}</b>')
    #gas.update_layout(hovermode="x unified")
    #gas.update_layout(yaxis1=dict(type='log'))
    
    # update trace
    gas.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update axis
    gas.update_yaxes(title_text="<b>Gas (Cubic Meters per Day)</b>", nticks=10)
    gas.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols3[1].plotly_chart(gas)
    
    #FILA 2
    cols4 = st.columns(2)
    
    ##WATER PROD##
    w_prod = px.scatter(filtrado, x= filtrado.index, y="agua_bpd", log_y=False, color="terminacion")
    
    # update layout
    w_prod.update_layout(title=f'<b>Water Production - {camp}</b>')
    #w_prod.update_layout(hovermode="x unified")
    #w_prod.update_layout(yaxis1=dict(type='log'))
    
    # update trace
    w_prod.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update axis
    w_prod.update_yaxes(title_text="<b>Water Production (Barrels Per Day)</b>", nticks=10)
    w_prod.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols4[0].plotly_chart(w_prod)
    
    ##WATER_CUT##
    w_cut = px.scatter(filtrado, x= filtrado.index, y="water_cut", log_y=False, color="terminacion")
    
    # update trace
    w_cut.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update layout
    w_cut.update_layout(title=f'<b>Water Cut - {camp}</b>')
    #w_cut.update_layout(hovermode="x unified")
    #w_cut.update_layout(yaxis1=dict(type='log'))
    
    # update axis
    w_cut.update_yaxes(title_text="<b>Water Cut (%)</b>", nticks=10)
    w_cut.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols4[1].plotly_chart(w_cut)

    #FILA 3
    cols5 = st.columns(2)
    
    ##PRESS 1##
    press_1 = px.scatter(filtrado_press, x= filtrado_press.index, y="cerrado(yac)", log_y=False, color="terminacion")
    
    # update trace
    press_1.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update layout
    press_1.update_layout(title=f'<b>Reservoir Pressure (Plugged) - {camp}</b>')
    press_1.update_layout(hovermode="x unified")
    #press_1.update_layout(yaxis1=dict(type='log'))
    
    # update axis
    press_1.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b>", nticks=10)
    press_1.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols5[0].plotly_chart(press_1)

    ##PRESS 2##
    press_2 = px.scatter(filtrado_press, x= filtrado_press.index, y="cerrado(pozo)", log_y=False, color="terminacion")
    
    # update trace
    press_2.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update layout
    press_2.update_layout(title=f'<b>Well Pressure (Plugged) - {camp}</b>')
    press_2.update_layout(hovermode="x unified")
    #press_2.update_layout(yaxis1=dict(type='log'))
    
    # update axis
    press_2.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b>", nticks=10)
    press_2.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols5[1].plotly_chart(press_2)
    
    
    #FILA 4
    cols6 = st.columns(2)
    
    ##PRESS 3##
    press_3 = px.scatter(filtrado_press, x= filtrado_press.index, y='fluyendo(yac)', log_y=False, color="terminacion")
    
    # update trace
    press_3.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update layout
    press_3.update_layout(title=f'<b>Reservoir Pressure - {camp}</b>')
    press_3.update_layout(hovermode="x unified")
    #press_3.update_layout(yaxis1=dict(type='log'))
    
    # update axis
    press_3.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b>", nticks=10)
    press_3.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols6[0].plotly_chart(press_3)

    ##PRESS 4##
    press_4 = px.scatter(filtrado_press, x= filtrado_press.index, y='fluyendo(pozo)', log_y=False, color="terminacion")
    
    # update trace
    press_4.update_traces(marker=dict(size=6, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # update layout
    press_4.update_layout(title=f'<b>Well Pressure - {camp}</b>')
    press_4.update_layout(hovermode="x unified")
    #press_4.update_layout(yaxis1=dict(type='log'))
    
    # update axis
    press_4.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b>", nticks=10)
    press_4.update_xaxes(title_text="<b>Year</b>", nticks=20)
    cols6[1].plotly_chart(press_4)
    
######################################################################################################

    # POZO PLOT
    
    pozo_plot_vs = st.columns(2)
    st.subheader(f'Historical and Calculated Production {well}')
    well_prod = make_subplots(specs=[[{"secondary_y": True}]])
    
    well_prod.add_trace(go.Scatter(x=data1['fecha'], y=data1['aceite_bpd'], mode='markers', marker_symbol = 'diamond', marker_line_width=.5, marker=dict(size=5,color='green'),name='Oil'),secondary_y=False)
    well_prod.add_trace(go.Scatter(x=data1['fecha'], y=data1['agua_bpd'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='blue'), name='Water'), secondary_y=False)
    well_prod.add_trace(go.Scatter(x=data1['fecha'], y=data1['gas'], mode='markers', marker_symbol = 'triangle-up', marker_line_width=.5, marker=dict(size=5,color='red'),name='Gas'),secondary_y=True)

    well_prod.add_trace(go.Scatter(x=data1['fecha'], y=data1['aceite_bpd'], mode='markers',marker_line_width=.5,marker=dict(size=5,color='purple'),name='Open'),secondary_y=False)
    well_prod.add_trace(go.Scatter(x=data2.index,y=data2['Open_Interval'],mode='markers',marker_line_width=.5,marker=dict(size=5,color='orange'),name='Open Interval'),secondary_y=False)
    
    # Set layout
    well_prod.update_layout(title_text = f'Historical Production {well}')
    #well_prod.update_layout(yaxis1=dict(type='log'))
    well_prod.update_layout(hovermode="x unified")
    well_prod.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,xanchor="right",x=1))
    well_prod.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    
    # update x and y - axis
    well_prod.update_xaxes(title_text="<b>Year</b>")
    well_prod.update_yaxes(title_text="<b>Oil Production Rate [bbls/d] / Water Production Rate [bbl/d] </b> ", secondary_y=False)
    well_prod.update_yaxes(title_text="<b> Gas Production Rate [Cubic Meters per Day] </b>", secondary_y=True)
    well_prod.update_yaxes(nticks=10,secondary_y=False)
    well_prod.update_yaxes(nticks=10,secondary_y=True)
    well_prod.update_xaxes(nticks=50)
    
    pozo_plot_vs[0].plotly_chart(well_prod)
    
    well_prod_2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    well_prod_2.add_trace(go.Scatter(x=data1['fecha'], y=data1['aceite_bpd'], mode='markers', marker_symbol = 'diamond', marker_line_width=.5, marker=dict(size=5,color='green'),name='Oil'),secondary_y=False)
    well_prod_2.add_trace(go.Scatter(x=data1['fecha'], y=data1['agua_bpd'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='blue'), name='Water'), secondary_y=False)
    well_prod_2.add_trace(go.Scatter(x=data1['fecha'], y=data1['gas'], mode='markers', marker_symbol = 'triangle-up', marker_line_width=.5, marker=dict(size=5,color='red'),name='Gas'),secondary_y=True)

    well_prod.add_trace(go.Scatter(x=data1['fecha'], y=data1['aceite_bpd'], mode='markers',marker_line_width=.5,marker=dict(size=5,color='purple'),name='Open'),secondary_y=False)
    well_prod.add_trace(go.Scatter(x=data2.index,y=data2['Open_Interval'],mode='markers',marker_line_width=.5,marker=dict(size=5,color='orange'),name='Open Interval'),secondary_y=False)
    
    # Set layout
    well_prod_2.update_layout(yaxis1=dict(type='log'))
    well_prod_2.update_layout(hovermode="x unified")
    well_prod_2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    well_prod_2.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    
    # update x and y - axis
    well_prod_2.update_xaxes(title_text="<b>Year</b>")
    well_prod_2.update_yaxes(title_text="<b>Oil Production Rate [Barrels per Day] </b> ", secondary_y=False)
    well_prod_2.update_yaxes(title_text="<b> Gas Production Rate [Cubic Meters per Day] </b>", secondary_y=True)
    well_prod_2.update_yaxes(nticks=10,secondary_y=False)
    well_prod_2.update_yaxes(nticks=10,secondary_y=True)
    well_prod_2.update_xaxes(nticks=50)
    
    pozo_plot_vs[1].plotly_chart(well_prod_2)
    
    st.subheader("Well Historical Production: ")
    st.caption("Cum Oil: " + str(round(cum_pozo,2)) + " MMBO")
    st.caption("Cum Gas: " + str(round(cum_gas,2)) + " MMCF")
    st.caption("Cum Water: " + str(round(cum_agua,2)) + " MMB")
    
    if st.checkbox('Export Figure'):
        st.write(well_prod.write_html(f'Well graphic {well}.html', auto_open=True))
        st.write(well_prod_2.write_html(f'Well graphic {well}.html', auto_open=True))

######################################################################################################

with st.expander('Water Control Diagnostic Plots'):

    # Water control diagnostic - DATA 
    
    # GOR por campo
    filtrado['GOR'] = filtrado['gas_mmcfpd'] / filtrado['aceite_barrels']
    filtrado['GOR+1'] = (filtrado['gas_mmcfpm']+filtrado['aceite_barrels'])/filtrado['aceite_barrels']
    
    filtrado['WOR'] = filtrado['agua_bpm'] / filtrado['aceite_barrels']
    filtrado['WOR+1'] = (filtrado['agua_bpm']+filtrado['aceite_barrels'])/filtrado['aceite_barrels']
    
    filtrado['cum_days'] = filtrado['dias'].cumsum()
    
    field_wor = px.scatter(filtrado, x=filtrado.index, y="WOR", log_y=True, color="terminacion", width=1000)
    field_wor.update_traces(marker=dict(size=5, line=dict(width=.5)), selector=dict(mode='markers'))
    #fig2.update_traces(hoverinfo=['POZO', 'FECHA', 'SALININDAD', 'AGUA'], selector=dict(type='scatter'))
    
    # Set x-axis title
    field_wor.update_layout(hovermode= "x unified")
    field_wor.update_xaxes(title_text= "<b>Year</b>")
    #fig2.update_layout(legend=dict(orientation="v",yanchor="bottom",y=1,xanchor="right",x=1))
    
    # Set y-axes titles
    field_wor.update_layout(yaxis1=dict(type='log'))
    
    # update
    field_wor.update_layout(title_text=f'Historical WOR {camp} Field')
    field_wor.update_yaxes(title_text="<b>WOR</b>")
    field_wor.update_yaxes(nticks=20,color = 'black')
    field_wor.update_xaxes(nticks=20,color = 'black', calendar = 'gregorian')
    #salt_mont.layout.plot_bgcolor = '#F4F5F6'
    
    st.plotly_chart(field_wor)
    
    field_gor = px.scatter(filtrado, x=filtrado.index, y="GOR", log_y=False, color="terminacion", width=1000)
    field_gor.update_traces(marker=dict(size=5, line=dict(width=.5)), selector=dict(mode='markers'))
    #fig2.update_traces(hoverinfo=['POZO', 'FECHA', 'SALININDAD', 'AGUA'], selector=dict(type='scatter'))
    
    # Set x-axis title
    field_gor.update_layout(hovermode= "x unified")
    field_gor.update_xaxes(title_text= "<b>Year</b>")
    #field_gor.update_layout(yaxis_range=[filtrado.GOR.min, filtrado.GOR.max])
    #fig2.update_layout(legend=dict(orientation="v",yanchor="bottom",y=1,xanchor="right",x=1))
    
    # Set y-axes titles
    #field_gor.update_layout(yaxis1=dict(type='log'))
    
    # update
    field_gor.update_layout(title_text=f'Historical GOR {camp} Field')
    field_gor.update_yaxes(title_text="<b>GOR</b>")
    field_gor.update_yaxes(nticks=20,color = 'black')
    field_gor.update_xaxes(nticks=20,color = 'black', calendar = 'gregorian')
    #salt_mont.layout.plot_bgcolor = '#F4F5F6'
    
    st.plotly_chart(field_gor)
    
    # GOR por pozo
    data1['GOR'] = data1['gas_mmcfpm'] / data1['aceite_barrels']
    data1['GOR+1'] = (data1['gas_mmcfpm']+data1['aceite_barrels'])/data1['aceite_barrels']
    
    # WOR por pozo
    data1['WOR'] = data1['agua_bpm'] / data1['aceite_barrels']
    data1['WOR+1'] = (data1['agua_bpm']+data1['aceite_barrels'])/data1['aceite_barrels']
    
    data1['cum_days'] = data1['dias'].cumsum()
    #uwi = filtrado.terminacion[0]
    
    # salinity
    filtrado_salt_month = salt[salt['campo'] == camp]
    filtrado_salt_month.index = pd.DatetimeIndex(filtrado_salt_month.fecha)
    filtrado_salt_month['Day'] = filtrado_salt_month.index.day
    filtrado_salt_month['Month'] = filtrado_salt_month.index.month
    filtrado_salt_month['Year'] = filtrado_salt_month.index.year
    
    fil3= filtrado_salt_month.groupby(["Year"], as_index=False)['salinidad', 'water_cut', 'densidad', 'densidad_m'].sum()
    
    filtrado_salt = salt[salt['terminacion'] == well]
    filtrado_salt.index = pd.DatetimeIndex(filtrado_salt.fecha)
    filtrado_salt['Day'] = filtrado_salt.index.day
    filtrado_salt['Month'] = filtrado_salt.index.month
    filtrado_salt['Year'] = filtrado_salt.index.year
    
    fil4= filtrado_salt.groupby(["Year"], as_index=False)['salinidad', 'water_cut', 'densidad', 'densidad_m'].sum()
        
    ######################################################################################################
    
    # Water control diagnostic - PLOTS 
    
    cols7 = st.columns(2)
    
    wor = make_subplots(specs=[[{"secondary_y": False}]])
        
    wor.add_trace(go.Scatter(x=data1['fecha'], y=data1['WOR'], mode='markers', marker_line_width=.3, marker=dict(size=4,color='skyblue'), name= 'WOR'))
    wor.add_trace(go.Scatter(x=data1.cum_days, y=data1['WOR+1'], mode='markers', marker_line_width=.3, marker=dict(size=4,color='darkblue'), name= 'WOR+1'))
    
    # Set x-axis title
    wor.update_layout(hovermode="x unified")
    wor.update_xaxes(title_text="<b>Days</b>")
    wor.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    # Set y-axes titles
    # update
    
    wor.update_layout(title_text=f'Chan plot {well}')
    wor.update_yaxes(title_text="<b>WOR/WOR'</b>")
    wor.update_yaxes(nticks=9)
    wor.update_yaxes(type="log")
    wor.update_xaxes(type="log")
        
    cols7[0].plotly_chart(wor)
    
    gor = make_subplots(specs=[[{"secondary_y": False}]])
        
    gor.add_trace(go.Scatter(x=data1['fecha'], y=data1['GOR'], mode='markers', marker_line_width=.3, marker=dict(size=4, color='red'), name= 'GOR'))
    gor.add_trace(go.Scatter(x=data1.cum_days, y=data1['GOR+1'], mode='markers', marker_line_width=.3, marker=dict(size=4, color='darkred'), name= 'GOR+1'))
    #gor = px.scatter(data1, x= 'cum_days', y="GOR", log_y=True, color="GOR", trendline="ols", color_continuous_scale=('Inferno'))
    #gor.add_scatter(data1, x="fecha", y="GOR+1", color="GOR+1", trendline="ols", color_continuous_scale=('Inferno'))
    
    # update trace
    gor.update_traces(marker=dict(size=5, line=dict(width=.4, color='DarkSlateGrey')), selector=dict(mode='markers'))
    
    # Set x-axis title
    gor.update_layout(hovermode="x unified")
    gor.update_xaxes(title_text="<b>Days</b>")
    gor.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    # Set y-axes titles
    # update
    
    gor.update_layout(title_text=f'Chan plot {well}')
    gor.update_yaxes(title_text="<b>GOR/GOR'</b>")
    gor.update_yaxes(nticks=9)
    gor.update_yaxes(type="log")
    gor.update_xaxes(type="log")
        
    cols7[1].plotly_chart(gor)
    
    # historical salinity
    
    salt_mont = px.scatter(filtrado_salt_month, x=filtrado_salt_month.index, y="salinidad", log_y=True, color="terminacion", width=1000)
    salt_mont.update_traces(marker=dict(size=5, line=dict(width=.5)), selector=dict(mode='markers'))
    #fig2.update_traces(hoverinfo=['POZO', 'FECHA', 'SALININDAD', 'AGUA'], selector=dict(type='scatter'))
    
    # Set x-axis title
    salt_mont.update_layout(hovermode= "x unified")
    salt_mont.update_xaxes(title_text= "<b>Year</b>")
    #fig2.update_layout(legend=dict(orientation="v",yanchor="bottom",y=1,xanchor="right",x=1))
    
    # Set y-axes titles
    salt_mont.update_layout(yaxis1=dict(type='log'))
    
    # update
    salt_mont.update_layout(title_text=f'Historical Salinity {camp} Field')
    salt_mont.update_yaxes(title_text="<b>Salinity (PPM)</b>")
    salt_mont.update_yaxes(nticks=20,color = 'black')
    salt_mont.update_xaxes(nticks=20,color = 'black', calendar = 'gregorian')
    #salt_mont.layout.plot_bgcolor = '#F4F5F6'
    
    st.plotly_chart(salt_mont)  
    
######################################################################################################
    
    #filtrado_salt['fecha2'] = pd.to_datetime(filtrado_salt['fecha'])
    
    salt_plt = make_subplots(specs=[[{"secondary_y": True}]])

    salt_plt.add_trace(go.Scatter(x=filtrado_salt['fecha'],y=filtrado_salt['salinidad'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='purple'),name='Salinity'), secondary_y=False)
    salt_plt.add_trace(go.Scatter(x=filtrado_salt['fecha'],y=filtrado_salt['water_cut'],mode='markers', marker_line_width=.5,marker=dict(size=4,color='blue'),name='Water<br>Cut'), secondary_y=True)
    
    # Set x-axis title
    salt_plt.update_layout(title=f'Historical Salinity {well}', hovermode="x unified")
    salt_plt.update_xaxes(title_text="<b>Year</b>")
    salt_plt.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, height=500, width=1000)
    # Set y-axes titles
    salt_plt.update_layout(yaxis1=dict(type='log'))
    # update
    salt_plt.update_yaxes(title_text="<b>Salinity (PPM)</b> ", secondary_y=False)
    salt_plt.update_yaxes(title_text="<b>Fw %</b>", secondary_y=True)
    salt_plt.update_yaxes(nticks=20,secondary_y=False)
    salt_plt.update_yaxes(nticks=20,secondary_y=True)
    salt_plt.update_xaxes(nticks=20, calendar = 'gregorian')
    
    st.plotly_chart(salt_plt)

######################################################################################################

 ######################################################################################################
    
with st.expander('Gas Cap Calculations'):
    GC_campo = filtrado.copy()
    GC_campo['fecha'] = pd.to_datetime(GC_campo.fecha)
    start_date = '31-12-2005'
    end_date = '31-12-2021'
    filter_dates = (GC_campo['fecha'] > start_date) & (GC_campo['fecha'] <= end_date)
    GC_campo = GC_campo.loc[filter_dates]
    st.write(GC_campo)
    
    samplot = px.scatter(GC_campo, x='fecha', y='gas', color='terminacion')
    st.plotly_chart(samplot)
    
    GC_gas = (GC_campo['gas'].sum())
    st.caption("Cum Gas: " + str(round(GC_gas, 2)/MM) + ' MMCM')
    st.caption("Cum Gas: " + str(round(GC_gas, 2)) + ' Cubic Meters')
    #samplot2

    #Project statistics
    
with st.expander('Project Statistics'):
    #Histogram
        
    bars_pie_water = st.columns(2)
    
    bars_top_ten_oil = px.bar(oilfields, x='campo', y='aceite_barrels', labels={'Well':'Oil Production'}, width=1510)
    bars_top_ten_oil.update_xaxes(title_text="Oilfield")
    bars_top_ten_oil.update_yaxes(title_text="Total Oil Produced (BOPD)")
    bars_top_ten_oil.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_oil.update_layout(title_text='Top 15 Oil Producer Fields')
    
    #bars_top_ten_oil.update_layout(autosize=True, yaxis=dict(title_text="Y-axis Title")
                
    st.plotly_chart(bars_top_ten_oil)
    
    bars_pie_oil = st.columns(2)
            
    bars_top_ten_gas = px.bar(gasfields, x='campo', y='gas_mmcfpd', labels={'Well':'Gas Production'}, width=1510)
    bars_top_ten_gas.update_xaxes(title_text="Oilfield")
    bars_top_ten_gas.update_yaxes(title_text="Total Gas Produced (mmcfpd)")
    bars_top_ten_gas.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_gas.update_layout(title_text='Top 15 Gas Producer Fields')
                
    st.plotly_chart(bars_top_ten_gas)
    
    bars_pie_gas = st.columns(2)

    bars_top_ten_water = px.bar(waterfields, x='campo', y='agua_bpd', labels={'Well':'Water Production'}, width=1510)
    bars_top_ten_water.update_xaxes(title_text="Oilfield")
    bars_top_ten_water.update_yaxes(title_text="Total Water Produced (BPD)")
    bars_top_ten_water.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_water.update_layout(title_text='Top 15 Water Producer fields')
                
    st.plotly_chart(bars_top_ten_water)
    
    bars_pie_water = st.columns(2)
    
######################################################################################################

    # All activo production stats
    
    #FILA 3
    #activo_stats = st.columns(2)
    
    #pies = filtrado.groupby(["fecha"], as_index=False)['aceite_bpd', 'gas_mmcfpd', 'agua_bpd'].sum()
    
    bars_top_ten_oilwell = px.bar(oilwells, x='aceite_barrels', y='terminacion', labels={'Well':'Oil Production'}, orientation='h', color='aceite_barrels', color_continuous_scale='RdBu')
    bars_top_ten_oilwell.update_xaxes(title_text="Well")
    bars_top_ten_oilwell.update_yaxes(title_text="Total Oil Produced (BOPD)")
    #bars_top_ten_oilwell.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_oilwell.update_layout(title_text='Top 25 Oil Producer Wells', yaxis={'categoryorder':'total ascending'})
    
    bars_pie_oil[1].plotly_chart(bars_top_ten_oilwell)
    
    pie_oil = px.pie(oilfields, names='campo', values='aceite_bpd', color='campo', color_discrete_sequence=px.colors.sequential.RdBu, title='Oil Production Rate')
    bars_pie_oil[0].plotly_chart(pie_oil)
    
    bars_top_ten_gaswell = px.bar(gaswells, x='gas_mmcfpd', y='terminacion', labels={'Well':'Gas Production'}, orientation='h', color='gas_mmcfpd', color_continuous_scale='RdBu')
    bars_top_ten_gaswell.update_xaxes(title_text="Well")
    bars_top_ten_gaswell.update_yaxes(title_text="Total Gas Produced (mmcfpd)")
    #bars_top_ten_oilwell.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_gaswell.update_layout(title_text='Top 25 Gas Producer Wells', yaxis={'categoryorder':'total ascending'})
    
    bars_pie_gas[1].plotly_chart(bars_top_ten_gaswell)
    
    pie_gas = px.pie(oilfields, names='campo', values='gas_mmcfpd', color='campo', color_discrete_sequence=px.colors.sequential.RdBu)
    bars_pie_gas[0].plotly_chart(pie_gas)
    
    bars_top_ten_waterwell = px.bar(waterwells, x='agua_bpd', y='terminacion', labels={'Well':'Water Production'}, orientation='h', color='agua_bpd', color_continuous_scale='RdBu')
    bars_top_ten_waterwell.update_xaxes(title_text="Well")
    bars_top_ten_waterwell.update_yaxes(title_text="Total Water Produced (bpd)")
    #bars_top_ten_oilwell.update_traces(marker_color='#82a1b8', marker_line_color='#132847', marker_line_width=1.5, opacity=0.6)
    bars_top_ten_waterwell.update_layout(title_text='Top 25 Water Producer Wells', yaxis={'categoryorder':'total ascending'})
    
    bars_pie_water[1].plotly_chart(bars_top_ten_waterwell)
    
    pie_water = px.pie(waterfields, names='campo', values='agua_bpd', color='campo', color_discrete_sequence=px.colors.sequential.RdBu)
    bars_pie_water[0].plotly_chart(pie_water)    
    
    
    #####NOTES#### map - hover cum_prod, shapes/colors (markers), pressure (wells) / instead of field ----- Saturation pressure, corregir los water control diagnostic plots