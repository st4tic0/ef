# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:54:41 2021

@author: IPSMX-L7NRKD03
"""

#################### EXPANDER 1 - CHECK RAW DATA ####################
with st.expander('Check Raw Data'):
    st.write(prod)
    st.write(press)
    st.write(coords)
    st.write(salt)

#################### EXPANDER 1 - PRODUCTION DATA PLOTS ####################
with st.expander('Production Data Plots'):
        
    # FIG 1, 2 - MAPA / BUBBLE MAP
    map_pozos_loc = px.scatter_mapbox(coords, lat="lat", lon="lon", hover_name="terminacion", zoom=8, color='campo')
    map_pozos_loc.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(map_pozos_loc)
    
    ### map_pozos_prod = BUBBLE MAP CON LOS POZOS DE SITIO GRANDE ###
    #
    
    # FIG 3 - PRODUCCION HISTORICA DEL CAMPO
    field_prod = make_subplots(specs=[[{"secondary_y": True}]])

    field_prod.add_trace(go.Scatter(x=campo_2['Year'], y=campo_2['Aceite_Anual'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='green'), name='Oil'), secondary_y=False)
    field_prod.add_trace(go.Scatter(x=campo_2['Year'], y=campo_2['Gas_Anual'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='red'), name='Gas'), secondary_y=False)
    field_prod.add_trace(go.Scatter(x=campo_2['Year'], y=campo_2['water_cut1'], mode='markers', marker_line_width=.5, marker=dict(size=4,color='blue'),name='Water<br>Cut'), secondary_y=True)
    
    # Set figure title and xaxis title
    field_prod.update_layout(title=f'<b>Oilfield Historical Production - {filt_campos}</b>', hovermode="x unified")
    field_prod.update_xaxes(title_text="<b>Year</b>")
    field_prod.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # Update yaxis layout
    field_prod.update_layout(yaxis1=dict(type='log'))
    
    # Set y-axes titles/layout
    field_prod.update_yaxes(title_text="<b>Oil (BOPD) / Gas (MMCFPD)</b> ", secondary_y=False)
    field_prod.update_yaxes(title_text="<b>Fw %</b>", secondary_y=True)
    field_prod.update_yaxes(nticks=10,secondary_y=False)
    field_prod.update_yaxes(nticks=10,secondary_y=True)
    field_prod.update_xaxes(nticks=50)
    
    st.plotly_chart(field_prod)
    
    #FIG 4 - PRESSURE PLOT (WELL VS RESERVOIR)
    field_press = make_subplots(specs=[[{"secondary_y": False}]])

    field_press.add_trace(go.Scatter(x=press_campo_2['Year'],y=press_campo_2['cerrado(yac)'], mode='lines', line={'dash': 'dash', 'color': 'black'}, name='Reservoir<br>Pressure<br>(plugged)'))
    field_press.add_trace(go.Scatter(x=press_campo_2['Year'],y=press_campo_2['cerrado(pozo)'], mode='lines', line={'dash': 'dash', 'color': 'red'}, name='Well<br>Pressure<br>(plugged)'))
    field_press.add_trace(go.Scatter(x=press_campo_2['Year'],y=press_campo_2['fluyendo(yac)'], mode='lines', line={'color': 'black'}, name='Reservoir<br>Pressure<br>(open)'))
    field_press.add_trace(go.Scatter(x=press_campo_2['Year'],y=press_campo_2['fluyendo(pozo)'], mode='lines', line={'color': 'red'}, name='Well<br>Pressure<br>(open)'))
    
    # Set x-axis title
    field_press.update_layout(title=f'<b>Oilfield Historical Pressure - {filt_campos}</b>', hovermode="x unified")
    field_press.update_xaxes(title_text="<b>Year</b>")
    field_press.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # Set y-axes titles
    field_press.update_layout(yaxis1=dict(type='log'))
    # update
    field_press.update_yaxes(title_text="<b>Pressure (Kg/cm3)</b> ", secondary_y=False)
    field_press.update_yaxes(nticks=10,secondary_y=True)
    field_press.update_xaxes(nticks=50)
    
    st.plotly_chart(field_press)