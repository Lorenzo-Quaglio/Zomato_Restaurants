#===========================================================================================
#     FUNCTIONS USED
#===========================================================================================


# 1) Substituir os valores de 'Country Code' pelo nome do país

def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
    return COUNTRIES[country_id]

# 2) Criação do Tipo de Categoria de Comida

def create_type_price(price_range):
    if price_range ==1:
        return "cheap"
    elif price_range == 2:
        return 'normal'
    elif price_range ==3:
        return 'expensive'
    else:
        return 'gourmet'
    
# 3) Criação do Nome das Cores

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
        return COLORS[color_code]
    
# 4) Renomear as colunas do Dataframe

import inflection

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# 5) Criação do Mapa --- Visão Geral

def country_maps (dados):

    import folium
    from folium.plugins import MarkerCluster
    from streamlit_folium import folium_static    

    df_aux = dados.loc[:, ['city', 'cuisines', 'latitude', 'longitude', 'restaurant_name', 'average_cost_for_two', 'aggregate_rating']]

    map = folium.Map()

    marker_cluster = MarkerCluster().add_to(map)

    for index, location_info in df_aux.iterrows():
        
        folium.Marker([location_info['latitude'], location_info['longitude']], 
                       popup=f"""
            <b>{location_info['restaurant_name']}</b><br>
            Cozinha: {location_info['cuisines']}<br>
            Preço médio para dois: {location_info['average_cost_for_two']}<br>
            Avaliação: {location_info['aggregate_rating']} / 5.0
            """
        ).add_to(marker_cluster)

    folium_static(map, width=1024, height=600)
    return None


# 6) Criação Gráfico 1 --- Visão Países

import plotly.express as px

def top_5_quant_rest(dados):
    
    # Agrupando por país e contando o número de restaurantes
    country_restaurant_count = dados.groupby('country_code')['restaurant_name'].count().reset_index()
    country_restaurant_count.columns = ['Países', 'restaurant_count']

    # Selecionando os top 5 países com maior quantidade de restaurantes
    top_countries = country_restaurant_count.nlargest(5, 'restaurant_count')
    
    # Criando as barras
    fig = px.bar(
        top_countries,
        x='Países',
        y='restaurant_count',
        title='Top 5 Países com Maior Número de Restaurantes Registrados',
        color='Países',
        text='restaurant_count',
        color_discrete_sequence=['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c', '#984ea3']
    )

    # Customizar a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
    title_font_size=30,
    title_font_color='white',
    xaxis_title='<br>Países',
    yaxis_title='Núm. Restaurantes<br>',
    yaxis=dict(
        showgrid=True,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing y-axis title font
    ),
    xaxis=dict(
        showgrid=False,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing x-axis title font
    ),
    font=dict(family="Cambria Math", size=12, color="white"),
    plot_bgcolor='#0e1117'
)
    
    return fig


# 7) Criação Gráfico 2 --- Visão Países

def top_5_quant_cidades(dados):
    
    # Agrupando por país e contando o número de restaurantes
    country_city_count = dados.groupby('country_code')['city'].nunique().reset_index()
    country_city_count.columns = ['Países', 'Cidades']
    
    # Selecionando os top 5 países com maior quantidade de cidades registradas
    top_countries_city = country_city_count.nlargest(5, 'Cidades')
    
    # Criando as barras
    fig = px.bar(
        top_countries_city,
        x='Países',
        y='Cidades',
        title='Top 5 Países com Maior Número de Cidades Registradas',
        color='Países',
        text='Cidades',
        color_discrete_sequence=['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c', '#984ea3']
    )

    # Customizar a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
    title_font_size=30,
    title_font_color='white',
    xaxis_title='<br>Países',
    yaxis_title='Cidades Registradas<br>',
    yaxis=dict(
        showgrid=True,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing y-axis title font
    ),
    xaxis=dict(
        showgrid=False,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing x-axis title font
    ),
    font=dict(family="Cambria Math", size=12, color="white"),
    plot_bgcolor='#0e1117'
)
    
    return fig


# 8) Criação Gráfico 3 --- Visão Países

def top_5_maior_aval(dados):
    
    # Agrupando por país e contando o número de restaurantes
    country_votes = dados.groupby('country_code')['votes'].sum().reset_index()
    country_votes.columns = ['Países', 'Avaliações']
    
    # Selecionando os top 5 países com maior quantidade de cidades registradas
    top_countries_votes = country_votes.nlargest(5, 'Avaliações')
    
    # Criando as barras
    fig = px.bar(
        top_countries_votes,
        x='Países',
        y='Avaliações',
        title='Quantidade de Avaliações por País',
        color='Países',
        text='Avaliações',
        color_discrete_sequence=['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c', '#984ea3']
    )

    # Customizar a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='none',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
    title_font_size=30,
    title_font_color='white',
    xaxis_title='<br>Países',
    yaxis_title='Avaliações Totais<br>',
    yaxis=dict(
        showgrid=True,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing y-axis title font
    ),
    xaxis=dict(
        showgrid=False,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing x-axis title font
    ),
    font=dict(family="Cambria Math", size=12, color="white"),
    plot_bgcolor='#0e1117'
)
    
    return fig


# 9) Criação Gráfico 4 --- Visão Países 

import pandas as pd

def top_5_media_prato(dados):
    
    # Garantir que a coluna 'average_cost_for_two' seja numérica
    dados['average_cost_for_two'] = pd.to_numeric(dados['average_cost_for_two'], errors='coerce')
    
    # Agrupando por país e contando o número de restaurantes
    country_votes = dados.groupby('country_code')['average_cost_for_two'].mean().reset_index()
    country_votes.columns = ['Países', 'Preço Médio']
    
    # Selecionando os top 5 países com maior quantidade de cidades registradas
    top_countries_votes = country_votes.nlargest(5, 'Preço Médio')
    
    # Criando as barras
    fig = px.bar(
        top_countries_votes,
        x='Países',
        y='Preço Médio',
        title='Média de Preço de um prato para 2 pessoas por país',
        color='Países',
        text='Preço Médio',
        color_discrete_sequence=['#377eb8', '#ff7f00', '#4daf4a', '#e41a1c', '#984ea3']
    )

    # Customizar a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='none',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
    title_font_size=30,
    title_font_color='white',
    xaxis_title='<br>Países',
    yaxis_title='Preço Médio<br>',
    yaxis=dict(
        showgrid=True,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing y-axis title font
    ),
    xaxis=dict(
        showgrid=False,
        title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizing x-axis title font
    ),
    font=dict(family="Cambria Math", size=12, color="white"),
    plot_bgcolor='#0e1117'
)
    
    return fig

# 10) Criação Gráfico 5 --- Visão Países 

def diversidade_gastronomica_treemap(dados):
    # Agrupando por país e contando o número de culinárias únicas
    country_cuisines = dados.groupby('country_code')['cuisines'].nunique().reset_index()
    country_cuisines.columns = ['País', 'Culinárias Únicas']

    # Criando o gráfico de treemap
    fig = px.treemap(
        country_cuisines,
        path=['País'], 
        values='Culinárias Únicas',
        color='Culinárias Únicas',
        color_continuous_scale=px.colors.diverging.RdBu,
        title='Diversidade Gastronômica - Quant. de Culinárias Únicas por País',
        labels={'Culinárias Únicas': 'Culinárias Únicas'}
    )

    # Customizando o texto para exibir o número de culinárias abaixo do nome do país
    fig.update_traces(texttemplate='<b>%{label}</b><br>%{value}')

    # Ajustando layout
    fig.update_layout(
        font=dict(family="Cambria Math", size=14, color="white"),
        title_font_size=24,
        title_font_color='white',
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        coloraxis_colorbar=dict(title="Culinárias Únicas")
    )

    return fig

# 11) Criação Gráfico 1 --- Visão Cidades 

def cidade_com_mais_restaurantes_por_pais(dados):
    # Agrupando por país e cidade, contando o número de restaurantes em cada cidade
    cidade_restaurantes = dados.groupby(['country_code', 'city'])['restaurant_name'].count().reset_index()
    cidade_restaurantes.columns = ['País', 'Cidade', 'Número de Restaurantes']
    
    # Encontrando a cidade com o maior número de restaurantes para cada país
    top_cidade_por_pais = cidade_restaurantes.loc[cidade_restaurantes.groupby('País')['Número de Restaurantes'].idxmax()]
    
    # Selecionando os top 10 cidades com maior quantidade de restaurantes registradas
    top_10 = top_cidade_por_pais.nlargest(10, 'Número de Restaurantes')
    
    # Criando o gráfico de barras
    fig = px.bar(
        top_10,
        x='Cidade',
        y='Número de Restaurantes',
        color='País',
        text='Número de Restaurantes',
        title='Cidade com Mais Restaurantes em Cada País',
        color_discrete_sequence=px.colors.diverging.Spectral
    )

    # Customizando o layout
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1,
        opacity=0.9
    )

    fig.update_layout(
        title_font_size=24,
        title_font_color='white',
        xaxis_title='Cidades',
        yaxis_title='Número de Restaurantes',
        yaxis=dict(showgrid=True),
        xaxis=dict(showgrid=False),
        font=dict(family="Cambria Math", size=14, color="white"),
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        coloraxis_colorbar=dict(title="Cidade")
    )

    return fig

# 12) Criação Gráfico 2 --- Visão Cidades 

def top_10_cidades_melhor_avaliadas(dados):
    # Garantir que a coluna 'aggregate_rating' seja numérica
    dados['aggregate_rating'] = pd.to_numeric(dados['aggregate_rating'], errors='coerce')
    
    # Filtrar restaurantes com média de avaliação maior que 4
    dados_filtrados = dados[dados['aggregate_rating'] > 4]
    
    # Agrupando por cidade e calculando o número de restaurantes com média de avaliação maior que 4
    city_restaurant_count = dados_filtrados.groupby(['country_code', 'city'])['restaurant_name'].count().reset_index()
    city_restaurant_count.columns = ['País','Cidade', 'Qtd Restaurantes']
    
    # Selecionando as top 10 cidades
    top_cities = city_restaurant_count.nlargest(10, 'Qtd Restaurantes')
    
    # Criando as barras
    fig = px.bar(
        top_cities,
        x='Cidade',
        y='Qtd Restaurantes',
        title='Top 10 Cidades com Restaurantes com Média de Avaliação Maior que 4',
        color='País',
        text='Qtd Restaurantes',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customizando a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
        title_font_size=30,
        title_font_color='white',
        xaxis_title='<br>Cidades',
        yaxis_title='Núm. Restaurantes<br>',
        yaxis=dict(
            showgrid=True,
            title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizando fonte do título do eixo y
        ),
        xaxis=dict(
            showgrid=False,
            title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizando fonte do título do eixo x
        ),
        font=dict(family="Cambria Math", size=12, color="white"),
        plot_bgcolor='#0e1117'
    )
    
    return fig

# 13) Criação Gráfico 3 --- Visão Cidades 

def top_10_cidades_piores_avaliadas(dados):
    # Garantir que a coluna 'aggregate_rating' seja numérica
    dados['aggregate_rating'] = pd.to_numeric(dados['aggregate_rating'], errors='coerce')
    
    # Filtrar restaurantes com média de avaliação maior que 4
    dados_filtrados = dados[dados['aggregate_rating'] < 2.5]
    
    # Agrupando por cidade e calculando o número de restaurantes com média de avaliação maior que 4
    city_restaurant_count = dados_filtrados.groupby(['country_code', 'city'])['restaurant_name'].count().reset_index()
    city_restaurant_count.columns = ['País','Cidade', 'Qtd Restaurantes']
    
    # Selecionando as top 10 cidades
    top_cities = city_restaurant_count.nlargest(10, 'Qtd Restaurantes')
    
    # Criando as barras
    fig = px.bar(
        top_cities,
        x='Cidade',
        y='Qtd Restaurantes',
        title='Top 10 Cidades com Restaurantes com Média de Avaliação Menor que 2,5',
        color='País',
        text='Qtd Restaurantes',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customizando a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
        title_font_size=30,
        title_font_color='white',
        xaxis_title='<br>Cidades',
        yaxis_title='Núm. Restaurantes<br>',
        yaxis=dict(
            showgrid=True,
            title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizando fonte do título do eixo y
        ),
        xaxis=dict(
            showgrid=False,
            title_font=dict(family="Aptos Narrow", size=20, color="white")  # Customizando fonte do título do eixo x
        ),
        font=dict(family="Cambria Math", size=12, color="white"),
        plot_bgcolor='#0e1117'
    )
    
    return fig

# 14) Criação Gráfico 4 --- Visão Cidades 

def top_10_cidades_culinarias_distintas(dados):
    # Garantir que a coluna 'cuisines' seja tratada corretamente
    dados['cuisines'] = dados['cuisines'].fillna('Desconhecida')

    # Agrupando por cidade e contando os tipos distintos de culinária
    city_cuisines_count = dados.groupby(['country_code', 'city'])['cuisines'].nunique().reset_index()
    city_cuisines_count.columns = ['País', 'Cidade', 'Culinárias Distintas']

    # Selecionando as top 10 cidades com mais tipos de culinárias distintos
    top_cities = city_cuisines_count.nlargest(10, 'Culinárias Distintas')
    
    # Criando as barras
    fig = px.bar(
        top_cities,
        x='Cidade',
        y='Culinárias Distintas',
        title='Top 10 Cidades com Mais Tipos de Culinárias Distintas',
        color='País',
        text='Culinárias Distintas',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customizando a aparência
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0,
        opacity=1
    )

    fig.update_layout(
        title_font_size=30,
        title_font_color='white',
        xaxis_title='<br>Cidades',
        yaxis_title='Núm. de Culinárias Distintas<br>',
        yaxis=dict(
            showgrid=True,
            title_font=dict(family="Aptos Narrow", size=20, color="white")
        ),
        xaxis=dict(
            showgrid=False,
            title_font=dict(family="Aptos Narrow", size=20, color="white")
        ),
        font=dict(family="Cambria Math", size=12, color="white"),
        plot_bgcolor='#0e1117'
    )
    
    return fig

# 15) Criação Gráfico 5 --- Visão Cidades 

def quantidade_restaurantes_por_cidade(dados):
    # Garantir que a coluna 'aggregate_rating' seja numérica
    dados['aggregate_rating'] = pd.to_numeric(dados['aggregate_rating'], errors='coerce')
    
    # Agrupando por cidade e contando o número de restaurantes
    city_restaurant_count = dados.groupby(['country_code', 'city'])['restaurant_name'].count().reset_index()
    city_restaurant_count.columns = ['País','Cidade', 'Qtd Restaurantes']
    
    # Selecionando as top 10 cidades
    top_cities = city_restaurant_count.nlargest(5, 'Qtd Restaurantes')
    
    # Criando gráfico de rosca (donut chart)
    fig = px.pie(
        top_cities, 
        names='Cidade', 
        values='Qtd Restaurantes', 
        title='Quantidade de Restaurantes por Cidade',
        hole=0.5,  
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Customizando a aparência
    fig.update_traces(textinfo='percent+label')  # Mostrando porcentagem e nome da cidade
    fig.update_layout(
        title_font_size=30,
        title_font_color='white',
        font=dict(family="Cambria Math", size=12, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='#0e1117'
    )
    
    return fig

# 16) Obter os melhores restaurantescom as maiores avaliações: nome restaurante --- Visão Restaurantes 

def top_restaurante_por_posicao_categoria_restaurante(dados, posicao=1):
        
    # Filtrar restaurantes com avaliação maior que 4
    melhores_restaurantes = dados[dados['aggregate_rating'] > 4]

    # Ordenar por avaliação, do maior para o menor
    melhores_restaurantes = melhores_restaurantes.sort_values(by='aggregate_rating', ascending=False)

    # Garantir que a posição solicitada não ultrapasse o número de restaurantes disponíveis
    if posicao > len(melhores_restaurantes):
        return f"A posição {posicao} excede o número de restaurantes disponíveis."

    # Selecionar o restaurante na posição desejada
    restaurante_escolhido = melhores_restaurantes.iloc[posicao - 1]  # -1 para ajustar o índice da lista

    # Obter o nome e a pontuação do restaurante
    categoria = restaurante_escolhido['cuisines']
        
    return f"Categoria: {categoria}"

# 17) Obter os melhores restaurantescom as maiores avaliações: nome restaurante --- Visão Restaurantes 

def top_restaurante_por_posicao_nome_restaurante(dados, posicao=1):
        
    # Filtrar restaurantes com avaliação maior que 4
    melhores_restaurantes = dados[dados['aggregate_rating'] > 4]

    # Ordenar por avaliação, do maior para o menor
    melhores_restaurantes = melhores_restaurantes.sort_values(by='aggregate_rating', ascending=False)

    # Garantir que a posição solicitada não ultrapasse o número de restaurantes disponíveis
    if posicao > len(melhores_restaurantes):
        return f"A posição {posicao} excede o número de restaurantes disponíveis."

    # Selecionar o restaurante na posição desejada
    restaurante_escolhido = melhores_restaurantes.iloc[posicao - 1]  # -1 para ajustar o índice da lista

    # Obter o nome e a pontuação do restaurante
    nome_restaurante = restaurante_escolhido['restaurant_name']
    
    return nome_restaurante
    
# 18) Obter os melhores restaurantescom as maiores avaliações: avaliação restaurante --- Visão Restaurantes 

def top_restaurante_por_posicao_avalia_restaurante(dados, posicao=1):
        
    # Filtrar restaurantes com avaliação maior que 4
    melhores_restaurantes = dados[dados['aggregate_rating'] > 4]

    # Ordenar por avaliação, do maior para o menor
    melhores_restaurantes = melhores_restaurantes.sort_values(by='aggregate_rating', ascending=False)

    # Garantir que a posição solicitada não ultrapasse o número de restaurantes disponíveis
    if posicao > len(melhores_restaurantes):
        return f"A posição {posicao} excede o número de restaurantes disponíveis."

    # Selecionar o restaurante na posição desejada
    restaurante_escolhido = melhores_restaurantes.iloc[posicao - 1]  # -1 para ajustar o índice da lista

    # Obter a pontuação do restaurante
    avaliacao_restaurante = restaurante_escolhido['aggregate_rating']
    
    return f"Avaliação: {avaliacao_restaurante}"    


# 19) Gráfico de melhor e piores culinárias por nota --- Visão Restaurantes

def melhor_pior_culinaria (dados, ordem = True, quantidade = 0): 
    
    # Ordenar pela média de nota das culinárias
    culinarias = dados.groupby('cuisines')['aggregate_rating'].mean().reset_index()
    
    # Ordenar de acordo com o parâmetro ordem e pegar as 'quantidade' linhas
    culinarias = culinarias.sort_values('aggregate_rating', ascending=ordem).head(quantidade)
    
    # Criar o gráfico de barras
    fig = px.bar(culinarias, x='cuisines', y='aggregate_rating', 
                 title=f'Top {quantidade} {"Melhores" if not ordem else "Piores"} Tipos de Culinárias',
                 labels={'cuisines': 'Culinária', 'aggregate_rating': 'Nota Média'},
                 color_discrete_sequence=['#377eb8'] if not ordem else ['#e41a1c'])
    
    # Atualizar o layout do gráfico
    fig.update_layout(title_font_size=16, title_font_color='pink', plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
                      font=dict(color="white"), xaxis=dict(title='Tipo de Culinária'), yaxis=dict(title='Nota Média'))
    
    return fig


# 20) Gráfico para gerar o gráfico das culinárias mais ofertadas --- Visão Restaurantes

def grafico_culinarias_ofertadas(dc_filtrado, quant_culinarias=10):
    
    # Contar a quantidade de restaurantes por tipo de culinária
    culinarias_ofertadas = dc_filtrado['cuisines'].value_counts().reset_index()
    culinarias_ofertadas.columns = ['Culinária', 'Quantidade']
    
    # Selecionar as 10 mais ofertadas ou conforme o filtro
    top_culinarias = culinarias_ofertadas.head(quant_culinarias)
    
    # Criar o gráfico de barras horizontais
    fig = px.bar(
        top_culinarias,
        x='Quantidade',
        y='Culinária',
        text='Quantidade',
        orientation='h',
        title='Quantidade de tipos de culinárias',
        labels={'Culinária': 'Gastronomia', 'Quantidade': 'Quantidades de tipos de culinária'},
        color='Culinária'
    )
    
    # Customizar o layout do gráfico
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )
    fig.update_layout(
        title_font_size=24,
        title_font_color='pink',
        xaxis_title='',
        yaxis_title='',
        showlegend=False,
        font=dict(family="Cambria Math", size=14, color="white"),
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        bargap=0.15
    )
    
    return fig













