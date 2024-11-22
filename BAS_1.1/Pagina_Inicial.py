import streamlit as st # type: ignore



st.title("Bem vindo ao BAS")
st.write("Um software especializado em bioprocessamento de dados obtidos do growth profiler. Comece agora seu trabalho clicando em 'Importar Dados' e caso queira conhecer mais sobre nosso trabalho clique em 'Saiba Mais'.")





st.markdown("<br>" * 4, unsafe_allow_html=True)
colunas = st.columns(4)

with colunas[3]: 
    if st.button("Importar Dados"):
        st.switch_page("pages/Importação_&_Seleção.py")


with colunas[0]: 
    if st.button("Saiba Mais"):
        st.switch_page("pages/Ver_Mais.py")






st.sidebar.markdown("<br>" * 12, unsafe_allow_html=True)


url_imagem = "https://github.com/BioAssis/BAS/blob/main/BAS_1.1/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)