# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:54:41 2021

@author: IPSMX-L7NRKD03
"""

#################### MAPA Y TABLA ####################

for_map = pozo.copy()
for_map = for_map[['campo', 'terminacion', 'fecha', 'class', 'lon', 'lat', 'aceite', 'gas', 'agua', 'aceite_bpd', 'agua_bpd', 'gas_mmcfpd', 'water_cut']]
for_map['fecha'] = for_map['fecha'].dt.date
map_filt = for_map.dropna()
map_filt['fecha'] = pd.to_datetime(map_filt['fecha'], dayfirst=True).dt.strftime('%m-%Y')

#################### BARRAS Y PIE #################### 
oilwells = prod.groupby(['terminacion']).sum()
oilwells = oilwells.sort_values(by=['aceite_barrels'])
oilwells = oilwells.nlargest(25, 'aceite_barrels').reset_index()

oilfields = prod.groupby(['campo']).sum()
oilfields = oilfields.sort_values(by=['aceite_barrels'])
oilfields = oilfields.nlargest(15, 'aceite_barrels').reset_index()

gaswells = prod.groupby(['terminacion']).sum()
gaswells = gaswells.sort_values(by=['gas'])
gaswells = gaswells.nlargest(25, 'gas').reset_index()

gasfields = prod.groupby(['campo']).sum()
gasfields = gasfields.sort_values(by=['gas'])
gasfields = gasfields.nlargest(15, 'gas').reset_index()

waterwells = prod.groupby(['terminacion']).sum()
waterwells = waterwells.sort_values(by=['agua'])
waterwells = waterwells.nlargest(25, 'agua').reset_index()

waterfields = prod.groupby(['campo']).sum()
waterfields = waterfields.sort_values(by=['agua_bpd'])
waterfields = waterfields.nlargest(15, 'agua_bpd').reset_index()

#################### SUBDATA POZOS ####################
MM = 1000000

r = pd.date_range(start=min(pozo.fecha), end = max(pozo.fecha), freq='M')
start = min(str(pozo.fecha))
pozo.index = pd.DatetimeIndex(pozo.fecha)
pozo = pozo.reindex(r, fill_value=0)
pozo['fecha'] = pozo.index
pozo['Mo'] = np.arange(len(pozo)) + 1
pozo['Yr'] = pozo['Mo'] / 12

f = pd.date_range(start='11/30/2021', end='12/31/2031', freq='M')

datad = np.random.randint(1, high=100, size=len(f))

# Copia del df -> pozo pero con nuevas columnas
pozo_2 = pd.DataFrame({'fecha': f, 'col2': datad})
pozo_2 = pozo_2.set_index('fecha')
pozo_2['Mo'] = np.arange(len(data2)) + 1
pozo_2['Yr'] = data2['Mo'] / 12
del pozo_2['col2']

# Calculos de acumulado
cum_oil = (pozo['aceite_bpd'].sum() * 30.5)/MM
cum_gas = (pozo['gas'].sum()*30.5)/MM
cum_agua = (pozo['agua_bpd'].sum()*30.5)/MM

# Calculo de la curva de tendencia
pozo['Historical trend'] = max(data1['aceite_bpd']) / (1 + 0.000000001 * di * data1['Yr']) ** (1 /0.000000001)

# Calculo de nuevas columnas a 'pozo_2'
pozo_2['Open'] = 100 / (1 + 0.000000001 * di * pozo_2['Yr']) ** (1 /0.000000001)
pozo_2['Open_Interval'] = 202 / (1 + 0.000000001 * di * pozo_2['Yr']) ** (1 /0.000000001)
pozo_2['Reentry'] = 607 / (1 + 0.000000001 * di * pozo_2['Yr']) ** (1 /0.000000001)

pozo_2['Open'] = np.where(pozo_2['Open']<= 10 , np.nan, data2['Open'])
pozo_2['Open_Interval'] = np.where(pozo_2['Open_Interval']<= 10 , np.nan, pozo_2['Open_Interval'])
pozo_2['Reentry'] = np.where(pozo_2['Reentry']<= 10 , np.nan, pozo_2['Reentry'])

pozo_2['Day'] = pozo_2.index.day
pozo_2['Month'] = pozo_2.index.month
pozo_2['Year'] = pozo_2.index.year

# Copia de df con mismos valores que 'pozo_2'
pozo_3 = pozo_2
pozo_4 = pozo_2

# Indexar fecha en las nuevas variables
pozo_3['Day'] = pozo_2.index.day
pozo_3['Month'] = pozo_2.index.month
pozo_3['Year'] = pozo_2.index.year
pozo_4['Day'] = pozo_2.index.day
pozo_4['Month'] = pozo_2.index.month
pozo_4['Year'] = pozo_2.index.year
pozo_2['Price'] = 60
pozo_2['Open_monthly'] = pozo_2['Open'] * pozo_2['Day']
pozo_2['Open_Interval_monthly'] = pozo_2['Open_Interval'] * pozo_2['Day']
pozo_2['Reentry_monthly'] = pozo_2['Reentry'] * pozo_2['Day']
pozo_2['Revenue_Open'] = 60 * pozo_2['Open'] * pozo_2['Day']
pozo_2['Revenue_Open_Interval'] = 60 * pozo_2['Open_Interval'] * pozo_2['Day'] 
pozo_2['Revenue_Reentry'] = 60 * pozo_2['Reentry'] * pozo_2['Day']

pozo_3 = pozo_2.groupby(["Year",'Month'], as_index=False)['Open_monthly','Revenue_Open'].sum()

pozo_4 = pozo_2.groupby(["Year",'Month'], as_index=False)['Open_Interval_monthly','Revenue_Open_Interval'].sum()

pozo_5 = pozo_2.groupby(["Year",'Month'], as_index=False)['Reentry_monthly','Revenue_Reentry'].sum()

#################### SUBDATA CAMPOS ####################
#del filtrado['water_cut']
campo.index = pd.DatetimeIndex(campo.fecha)
campo['Aceite_Anual'] = campo['aceite_barrels'] * campo['dias']
campo['Gas_Anual'] = campo['gas_mmcfpd'] * campo['dias']
campo['Agua_Anual'] = campo['agua_bpd'] * campo['dias']
campo['Day'] = campo.index.day
campo['Month'] = campo.index.month
campo['Year'] = campo.index.year
    
      
campo_2 = campo.groupby(["Year"], as_index=False)['Aceite_Anual','Gas_Anual','Agua_Anual'].sum() ###FIL###
campo_2['water_cut1'] = campo_2['Agua_Anual'] / (campo_2['Agua_Anual']+campo_2['Aceite_Anual']) 

#################### SUBDATA FIELD PRESSURE ####################
press_campo = press_campo[press_campo['campo'] == camp]
press_campo.index = pd.DatetimeIndex(press_campo.fecha)
press_campo['Day'] = press_campo.index.day
press_campo['Month'] = press_campo.index.month
press_campo['Year'] = press_campo.index.year

press_campo_2 = filtrado_press.groupby(["Year"], as_index=False)['cerrado(yac)', 'cerrado(pozo)', 'fluyendo(yac)', 'fluyendo(pozo)'].sum() ###FIL2###
#'cerrado(yac)', 'cerrado(pozo)', 'fluyendo(yac)', 'fluyendo(pozo)'#

#################### SUBDATA GOR/WOR ####################
pozo['GOR'] = pozo['gas'] / pozo['aceite_barrels']
pozo['GOR+1'] = (pozo['gas'] + pozo['aceite_barrels']) / pozo['aceite_barrels']
pozo['WOR'] = pozo['agua_bpm'] / pozo['aceite_barrels']
pozo['WOR+1'] = (pozo['agua_bpm'] + pozo['aceite_barrels']) / pozo['aceite_barrels']
pozo['cum_days'] = pozo['dias'].cumsum()

#################### SUBDATA SALINITY ####################
salt_campo = salt[salt['campo'] == camp]
salt_campo.index = pd.DatetimeIndex(salt_campo.fecha)
salt_campo['Day'] = salt_campo.index.day
salt_campo['Month'] = salt_campo.index.month
salt_campo['Year'] = salt_campo.index.year

salt_campo_2 = salt_campo.groupby(["Year"], as_index=False)['salinidad', 'water_cut', 'densidad', 'densidad_m'].sum()