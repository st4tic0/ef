# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:54:41 2021

@author: IPSMX-L7NRKD03
"""

#################### SIDEBAR ELEMENT 1 - DATA LOADERS ####################
with st.sidebar.expander('Load Data'):
    uploadedfile = st.file_uploader('Production Data', type=['csv'], key=('Production'))
    prod = load_production_data(uploadedfile)
    
    uploadedfile1 = st.file_uploader('Pressure Data', type=['csv'], key=('Pressure'))
    press = load_pressure_data(uploadedfile1)
    
    uploadedfile2 = st.file_uploader('Coordinates', type=['csv'], key=('Maps'))
    coords = load_mapa_coords(uploadedfile2)

    uploadedfile3 = st.file_uploader('Salinity', type=['csv'], key=('salt'))
    salt = load_salt_data(uploadedfile3)

#################### SIDEBAR ELEMENT 2 - DATA FILTER/SELECTORS ####################
with st.sidebar.expander('Well Selector'):
    campos = prod['campo'].unique()
    filt_campos = st.selectbox('Select an oilfield', campos)
    
    campo = prod[prod['campo'] == filt_campos]
    
    pozos = campo['terminacion'].unique()
    filt_pozos = st.selectbox('Select a well', pozos)
    
    pozo = selected_camp[selected_camp['terminacion'] == filt_pozos]
    
#################### SIDEBAR ELEMENT 3 - DECLINATION CURVE ANALYTIC TOOLS ####################
with st.sidebar.expander('Declination Curve Analytics'):
    #di = st.sidebar.slider('Di value',0.0, 1.0, (0.130),0.005)
    di = st.number_input('Declination Index Value: ')
    capex = st.number_input('Enter a CAPEX value')
    opening = st.checkbox('CAPEX Reopen Well')
    interval = st.checkbox('CAPEX New Interval')
    reentry= st.checkbox('CAPEX Re-entry')