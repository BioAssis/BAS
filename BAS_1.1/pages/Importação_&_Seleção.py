import streamlit as st
import funcoes.funcoes_importar_selecionar as fn


st.title("Importação & Seleção")
st.write("Nessa página você poderá importar os arquivos que deseja trabalhar e selecionar os poços que mais te interessarem.")


fn.importar_e_selecionar()



# Criando o botão
if st.button("Tratamento de Dados"):
    st.switch_page("pages/Tratamento_&_Plotagem.py")






st.sidebar.markdown("<br>" * 12, unsafe_allow_html=True)

st.sidebar.image("/home/ABTLUS/daniel23020/Documentos/ILUM/4° Semestre/IP/BAS/BAS_1.1/midias/logo.jpeg", use_column_width=True)