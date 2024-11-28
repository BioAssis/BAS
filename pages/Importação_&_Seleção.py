import streamlit as st # type: ignore
import funcoes.funcoes_importar_selecionar as fn

st.set_page_config(page_title="Importaçãoe e Seleção", layout="wide", initial_sidebar_state="expanded")

st.title("Importação & Seleção")
st.write("Nessa página você poderá importar os arquivos que deseja trabalhar e selecionar os poços que mais te interessarem.")



fn.importar_e_selecionar()









url_imagem = "https://raw.githubusercontent.com/BioAssis/BAS/main/BAS/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)