import streamlit as st # type: ignore
import funcoes.funcoes_tratamento_plotagem as fn


st.set_page_config(page_title="Tratamento e Plotagem", layout="wide", initial_sidebar_state="collapsed")

st.title("Tratamento e Plotagem de Dados")
st.write("Aqui você poderá analisar os arquivos selecionados na pagina anterior e além disso editar a forma como eles serão mostrados.")








fn.iniciar_tratamento_plotagem()










#st.sidebar.markdown("<br>" * 18, unsafe_allow_html=True)

url_imagem = "https://raw.githubusercontent.com/BioAssis/BAS/main/BAS/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)