#===========================================================================================
#     FTC - FINAL PROJECT - RESTAURANTS VIEW
#===========================================================================================

# Importing Libraries

import pandas as pd
import streamlit as st 
import inflection
import numpy as np
from utils.functions import country_name, create_type_price, color_name, rename_columns,top_restaurante_por_posicao_nome_restaurante, top_restaurante_por_posicao_categoria_restaurante, top_restaurante_por_posicao_avalia_restaurante,melhor_pior_culinaria, grafico_culinarias_ofertadas
from tabulate import tabulate
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
from datetime import datetime


#==========================================================================================================
            # CONFIGURAÇÃO DA PÁGINA NO STREAMLIT
#==========================================================================================================

st.set_page_config(page_title='Visão Restaurantes', page_icon='🍴', layout='wide')

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

st.sidebar.markdown('#### Selecione a quantidade de tipos de restaurantes que deseja visualizar:')
quant_rest = st.sidebar.slider('', 0, len(dc['cuisines'].dropna().unique()), 10)

# Filtrar o DataFrame com base na quantidade selecionada
culinarias_selecionadas = dc['cuisines'].dropna().unique()[:quant_rest]
dc = dc[dc['cuisines'].isin(culinarias_selecionadas)]


st.sidebar.markdown('#### Escolha os tipos de culinária que deseja visualizar:')
culinary_options = st.sidebar.multiselect(
    "",
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza', 'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood', 'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food', 'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery', 'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak', 'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern', 'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary', 'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian', 'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African', 'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others', 'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental', 'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African', 'Drinks Only', 'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç'],
    default=['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza', 'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood', 'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food', 'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery', 'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak', 'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern', 'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary', 'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian', 'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African', 'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others', 'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental', 'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African', 'Drinks Only', 'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç']
)

# Filtrar o DataFrame com base nas opções selecionadas
dc_filtrado = dc[dc['cuisines'].isin(culinary_options)]



st.sidebar.markdown ("""---""")

st.sidebar.markdown ('### Powered by Lorenzo Quaglio')

#==========================================================================================================
            #LAYOUT NO STREAMLIT
#==========================================================================================================

st.markdown('<h1 style="color: tomato; text-align: center;">Zomato Restaurants</h1><br>', unsafe_allow_html=True)
st.markdown('<h3 style="color: white;text-align: center;">Encontre o lugar perfeito para descobrir seu próximo restaurante favorito!</h3>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<br><h3 style="color: tomato;text-align: left;">🍴 VISÃO RESTAURANTES</h3><br>', unsafe_allow_html=True)

with st.container():    
        st.markdown('<h3 style="color: white;text-align: center;">Melhores restaurantes das principais categorias culinárias<br></h3>', unsafe_allow_html=True)

        col_1, col_2, col_3, col_4, col_5 = st.columns(5)

        with col_1:
            top_1_restaurante = top_restaurante_por_posicao_nome_restaurante(dc_filtrado, 1)
            col_1.markdown(f'<h5 style="color: pink; text-align: center;">{top_1_restaurante}<br></h5>', unsafe_allow_html=True)
            
            top_1_culinaria = top_restaurante_por_posicao_categoria_restaurante(dc_filtrado, 1)
            st.markdown(f'<h6 style="color: white; text-align: center;">{top_1_culinaria}</h6>', unsafe_allow_html=True)

            top_1_avaliacao = top_restaurante_por_posicao_avalia_restaurante(dc_filtrado, 1)
            col_1.markdown(f'<h6 style="text-align: center;">{top_1_avaliacao}</h6>', unsafe_allow_html=True)

                
        with col_2:
            top_2_restaurante = top_restaurante_por_posicao_nome_restaurante(dc_filtrado, 2)
            col_2.markdown(f'<h5 style="color: pink; text-align: center;">{top_2_restaurante}<br></h5>', unsafe_allow_html=True)
            
            top_2_culinaria = top_restaurante_por_posicao_categoria_restaurante(dc_filtrado, 2)
            st.markdown(f'<h6 style="color: white; text-align: center;">{top_2_culinaria}</h6>', unsafe_allow_html=True)

            top_2_avaliacao = top_restaurante_por_posicao_avalia_restaurante(dc_filtrado, 2)
            col_2.markdown(f'<h6 style="text-align: center;">{top_2_avaliacao}</h6>', unsafe_allow_html=True)
            
        with col_3:
            top_3_restaurante = top_restaurante_por_posicao_nome_restaurante(dc_filtrado, 3)
            col_3.markdown(f'<h5 style="color: pink; text-align: center;">{top_3_restaurante}<br></h5>', unsafe_allow_html=True)
            
            top_3_culinaria = top_restaurante_por_posicao_categoria_restaurante(dc_filtrado, 3)
            st.markdown(f'<h6 style="color: white; text-align: center;">{top_3_culinaria}</h6>', unsafe_allow_html=True)

            top_3_avaliacao = top_restaurante_por_posicao_avalia_restaurante(dc_filtrado, 3)
            col_3.markdown(f'<h6 style="text-align: center;">{top_3_avaliacao}</h6>', unsafe_allow_html=True)

            
        with col_4:
            top_4_restaurante = top_restaurante_por_posicao_nome_restaurante(dc_filtrado, 4)
            col_4.markdown(f'<h5 style="color: pink; text-align: center;">{top_4_restaurante}<br></h5>', unsafe_allow_html=True)
            
            top_4_culinaria = top_restaurante_por_posicao_categoria_restaurante(dc_filtrado, 4)
            st.markdown(f'<h6 style="color: white; text-align: center;">{top_4_culinaria}</h6>', unsafe_allow_html=True)

            top_4_avaliacao = top_restaurante_por_posicao_avalia_restaurante(dc_filtrado, 4)
            col_4.markdown(f'<h6 style="text-align: center;">{top_4_avaliacao}</h6>', unsafe_allow_html=True)
            
        with col_5:
            top_5_restaurante = top_restaurante_por_posicao_nome_restaurante(dc_filtrado, 5)
            col_5.markdown(f'<h5 style="color: pink; text-align: center;">{top_5_restaurante}<br></h5>', unsafe_allow_html=True)
            
            top_5_culinaria = top_restaurante_por_posicao_categoria_restaurante(dc_filtrado, 5)
            st.markdown(f'<h6 style="color: white; text-align: center;">{top_5_culinaria}</h6>', unsafe_allow_html=True)

            top_5_avaliacao = top_restaurante_por_posicao_avalia_restaurante(dc_filtrado, 5)
            col_5.markdown(f'<h6 style="text-align: center;">{top_5_avaliacao}</h6>', unsafe_allow_html=True)

with st.container():
    st.markdown(f'<br><h4 style="color: white;text-align: center;">Top {quant_rest} Restaurantes</h4>', unsafe_allow_html=True)
    st.dataframe(dc_filtrado[['restaurant_id', 'restaurant_name','aggregate_rating', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'votes']].head(quant_rest).sort_values('aggregate_rating', ascending=False))


with st.container():    
        st.markdown('<h3 style="color: white;text-align: center;"><br>Melhores e piores tipos de culinárias registradas</h3>', unsafe_allow_html=True)

        col_1, col_2= st.columns(2)

        with col_1:
            melhor = melhor_pior_culinaria (dc_filtrado,ordem=False,quantidade= quant_rest)
            st.plotly_chart(melhor)
                
        with col_2:
            pior = melhor_pior_culinaria (dc_filtrado,ordem=True,quantidade= quant_rest)
            st.plotly_chart(pior)

with st.container():    
        st.markdown(f'<h3 style="color: white;text-align: center;"><br>As {quant_rest} Culinárias Mais Ofertadas</h3>', unsafe_allow_html=True)
        grafico = grafico_culinarias_ofertadas (dc_filtrado,quant_culinarias=quant_rest)
        st.plotly_chart(grafico)






























































