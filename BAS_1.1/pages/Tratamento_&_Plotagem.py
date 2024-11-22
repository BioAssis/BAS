import streamlit as st


st.title("Tratamento e Plotagem de Dados")
st.write("Aqui você poderá analisar os arquivos selecionados na pagina anterior e além disso editar a forma como eles serão mostrados.")






if st.button("Saiba Mais Sobre o Projeto"):
    st.switch_page("pages/Ver_Mais.py")


st.sidebar.markdown("<br>" * 12, unsafe_allow_html=True)

st.sidebar.image("/home/ABTLUS/daniel23020/Documentos/ILUM/4° Semestre/IP/BAS/BAS_1.1/midias/logo.jpeg", use_column_width=True)