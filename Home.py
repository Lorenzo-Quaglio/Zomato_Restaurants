# Home ZOMATO RESTAURANTS - Lorenzo Q.

# Libraries

import streamlit as st
from PIL import Image
import utils.functions

st.set_page_config(page_title='Home', page_icon='💼', layout='wide')

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

imagem = Image.open('profile_image.jpeg')
st.sidebar.image(imagem, width=120)

st.markdown('<h1 style="color: tomato; text-align: center;">Zomato Restaurants</h1><br>', unsafe_allow_html=True)

st.markdown('<h3 style="color: white;text-align: center;">Um projeto de Análise de Dados</h3>', unsafe_allow_html=True)
st.markdown ("""---""")

st.markdown('<h5 style="color: white;text-align: left;"><br>Neste espaço, você encontrará uma análise completa dos dados da Zomato Restaurants, que possui uma vasta rede de restaurantes ao redor do mundo, proporcionando uma riqueza de informações. <br><br>Este dashboard analítico foi desenvolvido com base em dados de diversos restaurantes espalhados globalmente.</h5>', unsafe_allow_html=True)

st.markdown('<h3 style="color: tomato;text-align: left;"><br>Como utilizar este dashboard?</h3>', unsafe_allow_html=True)

st.markdown("""######
- Os dados fornecidos incluem uma variedade de informações, com foco em qualidade, localização e disponibilidade.
    - Localização: os pontos geográficos estão distribuídos em um mapa-múndi, com detalhes sobre cada restaurante.
    - Qualidade: há filtros disponíveis para oferecer uma experiência personalizada, permitindo a segmentação por país e avaliações.
    - Disponibilidade: são fornecidos dados sobre entregas online, reservas, avaliações e preços.
- Todos os indicadores foram organizados e refinados para garantir informações precisas e diretas.
- No menu à esquerda, você pode navegar por todas as informações obtidas após o processo de Análise Descritiva e Estatística de Dados.
""")

st.markdown('<h3 style="color: tomato;text-align: left;"><br>Dúvidas? Sinta-se à vontade para falar comigo!</h3>', unsafe_allow_html=True)

st.markdown("""
###### 
- gmail: lorenzoquaglio@gmail.com
- LinkedIn: www.linkedin.com/in/lorenzo-quaglio-78919b180
""")