import streamlit as st # type: ignore
import funcoes.funcoes_tratamento_plotagem as fn

st.title("Tratamento e Plotagem de Dados")
st.write("Aqui você poderá analisar os arquivos selecionados na pagina anterior e além disso editar a forma como eles serão mostrados.")








fn.iniciar_tratamento_plotagem()











st.sidebar.markdown("<br>" * 11, unsafe_allow_html=True)

st.sidebar.image("/home/ABTLUS/daniel23020/Documentos/ILUM/4° Semestre/IP/BAS/BAS_1.1/midias/logo.jpeg", use_column_width=True)