# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:54:40 2021

@author: IPSMX-L7NRKD03
"""

@st.cache
#################### PRODUCTION DATA ####################
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

#################### PRESSURE DATA ####################
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

#################### COORDS ####################
def load_mapa_coords(uploadedfile_2):
    if uploadedfile_2:
        string = uploadedfile_2.read()
        coordinates = pd.read_csv(io.StringIO(string.decode('utf-8')))
        coordinates = coordinates.rename(columns={'LATITUD': 'lat', 'LONGITUD': 'lon'})
        coordinates = coordinates.loc[:, ~coordinates.columns.str.contains('^Unnamed')]
        coordinates.columns = [x.lower() for x in coordinates.columns]
        coordinates = coordinates.dropna(subset=['lon', 'lat'])

    else:
            coords = None
    
    return coords

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float

#################### SALINITY ####################
def load_salt_data(uploadedfile_3):
    if uploadedfile_3:
        string = uploadedfile_3.read()
        salinity_data = pd.read_csv(io.StringIO(string.decode('utf-8')))
        salinity_data = salt.loc[:, ~salinity_data.columns.str.contains('^Unnamed')]
        salinity_data.columns = [x.lower() for x in salinity_data.columns]
        salinity_data = salinity_data.fillna(0)
        salinity_data = salinity_data.rename(columns={"dens.": "densidad", "dens. m": "densidad_m"})
        salinity_data = salinity_data.rename(columns={'pozo': 'terminacion', 'agua': 'water_cut'})
        salinity_data["salinidad"] = salinity_data["salinidad"].astype('str')
        salinity_data['salinidad'] = salinity_data['salinidad'].str.replace(',','')
        salinity_data['salinidad'] = salinity_data['salinidad'].astype(float)
        salinity_data = salinity_data[salinity_data.salinidad >= 1]
        salinity_data = salinity_data[salinity_data.water_cut >= 1]

    else:
            salinity_data = None
    
    return salinity_data

pd.options.display.float_format = '{:,.2f}'.format

def format_float(value):
    return f'{value:,.2f}'

pd.options.display.float_format = format_float