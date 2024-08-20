#===========================================================================================
#     FTC - FINAL PROJECT - COUNTRIES VIEW
#===========================================================================================

# Importing Libraries

import pandas as pd
import streamlit as st 
import inflection
import numpy as np
from utils.functions import country_name, create_type_price, color_name, rename_columns, country_maps, top_5_quant_rest, top_5_quant_cidades, top_5_maior_aval,top_5_media_prato,diversidade_gastronomica_treemap
from tabulate import tabulate
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from datetime import datetime



#==========================================================================================================
            # CONFIGURAÇÃO DA PÁGINA NO STREAMLIT
#==========================================================================================================

st.set_page_config(page_title='Visão Países', page_icon='🌎', layout='wide')

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
st.markdown('<br><h3 style="color: tomato;text-align: left;">🌎 VISÃO PAÍSES</h3><br>', unsafe_allow_html=True)

with st.container():
    fig_1 = top_5_quant_rest(dc)
    st.plotly_chart(fig_1)
    
with st.container():
    fig_2 = top_5_quant_cidades(dc)
    st.plotly_chart(fig_2)

with st.container():
    col_1, col_2 = st.columns(2)
        
    with col_1:
        fig_3 = top_5_maior_aval(dc)
        st.plotly_chart(fig_3)
        
            
    with col_2:
        fig_4 = top_5_media_prato(dc)
        st.plotly_chart(fig_4)


with st.container():
    fig_5 = diversidade_gastronomica_treemap(dc)
    st.plotly_chart(fig_5)














