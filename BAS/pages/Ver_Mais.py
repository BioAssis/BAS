import streamlit as st # type: ignore
import funcoes.funcoes_ver_mais as fn

st.set_page_config(page_title="Sobre Nós", layout="wide", initial_sidebar_state="expanded")


st.title("Sobre Nós")

fn.iniciar_ver_mais()



#st.sidebar.markdown("<br>" * 18, unsafe_allow_html=True)


url_imagem = "https://raw.githubusercontent.com/BioAssis/BAS/main/BAS/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)