#===========================================================================================
#     FTC - FINAL PROJECT - GENERAL VIEW
#===========================================================================================

# Importing Libraries

import pandas as pd
import streamlit as st 
import inflection
import numpy as np
from utils.functions import country_name, create_type_price, color_name, rename_columns, country_maps
from tabulate import tabulate
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from datetime import datetime



#==========================================================================================================
            # CONFIGURAÇÃO DA PÁGINA NO STREAMLIT
#==========================================================================================================

st.set_page_config(page_title='Visão Geral', page_icon='📈', layout='wide')

page_bg_img = '''
<style>
body {
    background-color: #0e1117;
}
hr {
    border: 0;
    height: 3px;  /* Ajuste a espessura da linha */
    background: tomato;  /* Ajuste a cor da linha */
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

#==========================================================================================================
            # DATAFRAME
#==========================================================================================================

#----------------------------------------------------------------------------------------------------------
            # INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO
#----------------------------------------------------------------------------------------------------------

# 1) Carregando Dataframe

df = pd.read_csv("pages/zomato.csv")

#----------------------------------------------------------------------------------------------------------
#     LIMPEZA E EDIÇÃO DO DATAFRAME 
#----------------------------------------------------------------------------------------------------------

# 1) Renomeando as colunas

df = rename_columns(df)

# 2) Criando uma cópia do Dataframe Original para trabalhar

dc = df.copy()

# 3) Eliminar as linhas onde a coluna 'Cuisines' tem valores NaN

dc.dropna(subset=['cuisines'], inplace=True)

# 4) Trocando os nomes de todos os restaurantes por um único tipo de culinária

dc["cuisines"] = dc.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

# 5) Eliminar os itens duplicados oriundos da coluna ID

dc = dc.drop_duplicates(subset=['restaurant_id'])

# 6)) Substituir os valores de 'Country Code' pelo nome do país

dc['country_code'] = dc['country_code'].apply(country_name)

# 7) Criação do Tipo de Categoria de Comida

dc['price_range'] = dc['price_range'].apply(create_type_price)

# 8) Criação do Nome das Cores

dc['rating_color'] = dc['rating_color'].apply(color_name)

dc.reset_index()

# 9) Dataframe final de trabalho

#print(dc)

#==========================================================================================================
            #BARRA LATERAL NO STREAMLIT
#==========================================================================================================

imagem = Image.open('profile_image.jpeg')
st.sidebar.image (imagem, width = 120)

st.sidebar.markdown('<h3 style="color: tomato; ">ZOMATO RESTAURANTS</h3>', unsafe_allow_html=True)
st.sidebar.markdown ("""---""")

st.sidebar.markdown ('## Filtros')

st.sidebar.markdown(
    """
    <style>
    .stMultiSelect [data-baseweb="select"] {
        max-height: 100px; /* Ajuste este valor para definir a altura desejada */
        overflow-y: auto;
    }
    .stMultiSelect .css-1pahdxg-control {
        display: flex;
        justify-content: flex-start; /* Alinha o campo de filtro ao topo */
        align-items: flex-start; /* Alinha o campo de filtro ao topo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('#### Selecione os países cujos restaurantes você deseja visualizar:')
traffic_options = st.sidebar.multiselect(
    "",
    ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapore', 
     'United Arab Emirates', 'India', 'Indonesia', 'New Zealand', 'England', 'Qatar', 
     'South Africa', 'Sri Lanka', 'Turkey'],
    default=['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 
             'Singapore', 'United Arab Emirates', 'India', 'Indonesia', 'New Zealand', 
             'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey']
)

# Filtrar o DataFrame com base nas opções selecionadas
dc = dc[dc['country_code'].isin(traffic_options)]
st.sidebar.markdown ("""---""")

st.sidebar.markdown ('### Powered by Lorenzo Quaglio')

#==========================================================================================================
            #LAYOUT NO STREAMLIT
#==========================================================================================================

st.markdown('<h1 style="color: tomato; text-align: center;">Zomato Restaurants</h1><br>', unsafe_allow_html=True)
st.markdown('<h3 style="color: white;text-align: center;">Encontre o lugar perfeito para descobrir seu próximo restaurante favorito!</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<br><h4 style="color: tomato;text-align: left;">Aqui estão as marcas de restaurantes disponíveis na nossa plataforma, assim como, nossos principais indicadores:</h4><br>', unsafe_allow_html=True)

with st.container():    
        col_1, col_2, col_3, col_4, col_5 = st.columns(5)
        
        with col_1:
            st.markdown('<h6 style="color: pink; text-align: center; ">Restaurantes Cadastrados</h6>', unsafe_allow_html=True)
            G_1 = dc['restaurant_id'].nunique()   
            col_1.markdown(f'<h3 style="color: white;text-align: center;">{G_1}</h3>', unsafe_allow_html=True)
                
        with col_2:
            st.markdown('<h6 style="color: pink; text-align: center; ">Países Cadastrados</h6>', unsafe_allow_html=True)
            G_2 = dc['country_code'].nunique()
            col_2.markdown(f'<h3 style="color: white; text-align: center;">{G_2}</h3>', unsafe_allow_html=True)
            
        with col_3:
            st.markdown('<h6 style="color: pink; text-align: center; ">Cidades Cadastradas</h6>', unsafe_allow_html=True)
            G_3 = dc['city'].nunique()
            col_3.markdown(f'<h3 style="color: white; text-align: center;">{G_3}</h3>', unsafe_allow_html=True)

            
        with col_4:
            st.markdown('<h6 style="color: pink; text-align: center; "> Culinárias Oferecidas</h6>', unsafe_allow_html=True)
            G_5 = dc['cuisines'].nunique()
            col_4.markdown(f'<h3 style="color: white; text-align: center;">{G_5}</h3>', unsafe_allow_html=True)
            
        with col_5:
            st.markdown('<h6 style="color: pink; text-align: center; ">Avaliações na plataforma</h6>', unsafe_allow_html=True)
            G_4 = dc['votes'].sum()
            col_5.markdown(f'<h3 style="color: white; text-align: center;">{G_4}</h3>', unsafe_allow_html=True)

with st.container():
    st.markdown('<br><h4 style="color: pink;text-align: center;">Distribuição de nossos restaurantes no Mapa-Múndi:</h4>', unsafe_allow_html=True)
    st.markdown ('<h5 style="color: white;text-align: left;">Abaixo, você pode encontrar nossos restaurantes cadastrados perto de sua localidade!<br>Clicando com o mouse você pode analisar diversas informações como tipo de culinária, notas e preço médio para dois:</h5><br>', unsafe_allow_html=True)
    country_maps(dc)












 