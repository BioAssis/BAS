import streamlit as st # type: ignore
import funcoes.funcoes_importar_selecionar as fn


st.title("Importação & Seleção")
st.write("Nessa página você poderá importar os arquivos que deseja trabalhar e selecionar os poços que mais te interessarem.")



fn.importar_e_selecionar()








st.sidebar.markdown("<br>" * 11, unsafe_allow_html=True)


url_imagem = "https://raw.githubusercontent.com/BioAssis/BAS/main/BAS_1.1/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)