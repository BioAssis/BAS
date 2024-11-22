import streamlit as st # type: ignore
import funcoes.funcoes_tratamento_plotagem as fn

st.title("Tratamento e Plotagem de Dados")
st.write("Aqui você poderá analisar os arquivos selecionados na pagina anterior e além disso editar a forma como eles serão mostrados.")








fn.iniciar_tratamento_plotagem()











st.sidebar.markdown("<br>" * 11, unsafe_allow_html=True)

url_imagem = "https://github.com/BioAssis/BAS/blob/main/BAS_1.1/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)