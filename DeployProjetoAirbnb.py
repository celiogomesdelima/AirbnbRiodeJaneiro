#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import streamlit as st
import joblib
from pathlib import Path

#Variáveis que compõesm o modelo: 
#'host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
# 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'extra_people',
# 'minimum_nights', 'instant_bookable', 'ano', 'mes', 'num_amenities',
# 'property_type_Apartment', 'property_type_Bed and breakfast',
# 'property_type_Condominium', 'property_type_Guest suite',
# 'property_type_Guesthouse', 'property_type_Hostel',
# 'property_type_House', 'property_type_Loft', 'property_type_Other',
# 'property_type_Serviced apartment', 'room_type_Entire home/apt',
# 'room_type_Hotel room', 'room_type_Private room',
# 'room_type_Shared room', 'cancellation_policy_flexible',
# 'cancellation_policy_moderate', 'cancellation_policy_strict',
# 'cancellation_policy_strict_14_with_grace_period'

#organizando as variáveis por tipo:

x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 
               'beds': 0, 'extra_people': 0, 'minimum_nights': 0, 'ano': 0, 'mes': 0, 'num_amenities': 0, 'host_listings_count': 0}
x_binarios = {'host_is_superhost':0 , 'instant_bookable': 0 }
x_categorias = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium',  'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Other', 'Serviced apartment'], 
                'room_type':['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'], 
                'cancellation_policy': ['flexible', 'moderate', 'strict','strict_14_with_grace_period']}
resultado_x_categorias = {
    'property_type_Apartment':0, 
    'property_type_Bed and breakfast':0, 
    'property_type_Condominium':0, 
    'property_type_Guest suite': 0, 
    'property_type_Guesthouse': 0, 
    'property_type_Hostel':0,
    'property_type_House':0,
    'property_type_Loft':0, 
    'property_type_Other':0,
    'property_type_Serviced apartment':0,
    'room_type_Entire home/apt':0,
    'room_type_Hotel room':0,
    'room_type_Private room': 0,
    'room_type_Shared room': 0,
    'cancellation_policy_flexible': 0,
    'cancellation_policy_moderate': 0,
    'cancellation_policy_strict':0,
    'cancellation_policy_strict_14_with_grace_period':0
}


# In[3]:


for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step= 0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step= 0.01, value=0.0)
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor
    
for item in x_binarios:
    valor =  st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == 'Sim':
        x_binarios[item]=1
    else:
        x_binarios[item]=0

for item in x_categorias:
    valor =  st.selectbox(f'{item}', x_categorias[item])
    resultado_x_categorias[f'{item}_{valor}']=1

botao = st.button('Prever valor do imóvel')
if botao: 
    resultado_x_categorias.update(x_numericos)
    resultado_x_categorias.update(x_binarios)
    valores_x = pd.DataFrame(resultado_x_categorias, index=[0])
#Criando lista de colunas sem as colunas  'Unnamed: 0' e 'price'
    dados = pd.read_csv('C:/Users/Dell/Documents/GitHub/AirbnbRiodeJaneiro/dados.csv')
# Index(['Unnamed: 0', 'host_is_superhost', 'host_listings_count', 'latitude',
#        'longitude', 'accommodates', 'bathrooms', 'bedrooms', 'beds',
#        'extra_people', 'minimum_nights', 'instant_bookable', 'ano', 'mes',
#        'num_amenities', 'property_type_Apartment',
#        'property_type_Bed and breakfast', 'property_type_Condominium',
#        'property_type_Guest suite', 'property_type_Guesthouse',
#        'property_type_Hostel', 'property_type_House', 'property_type_Loft',
#        'property_type_Other', 'property_type_Serviced apartment',
#        'room_type_Entire home/apt', 'room_type_Hotel room',
#        'room_type_Private room', 'room_type_Shared room',
#        'cancellation_policy_flexible', 'cancellation_policy_moderate',
#        'cancellation_policy_strict',
#        'cancellation_policy_strict_14_with_grace_period', 'price'],
#       dtype='object')


#Criando lista de colunas sem as colunas  'Unnamed: 0' e 'price'
    colunas = list(dados.columns)[1:-1]
    
    #Reordenando valores_x na ordem das colunas do dados.csv
    valores_x = valores_x[colunas]
    
    modelo = joblib.load('C:/Users/Dell/Documents/GitHub/AirbnbRiodeJaneiro/modelo.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])

#Comando para rodar na minha máquina
#streamlit run C:\Users\Dell\Documents\GitHub\AirbnbRiodeJaneiro\DeployProjetoAirbnb.py

