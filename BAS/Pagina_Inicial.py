import streamlit as st # type: ignore

st.set_page_config(page_title="Pagina Inicial", layout="wide", initial_sidebar_state="expanded")


st.title("Bem vindo ao BAS")
st.write("""O BAS(Bioprocess Assistant Software) é um software especializado em bioprocessamento de dados obtidos do equipamento Growth Profiler. 
         Comece agora seu trabalho clicando em 'Importar Dados' ou caso queira conhecer mais sobre nosso trabalho e seus criadores clique em 'Saiba Mais'.""")



st.markdown("<br>" * 4, unsafe_allow_html=True)
colunas = st.columns(4)





st.session_state.clear()

  
with colunas[3]: 
    if st.button("Importar Dados"):
        st.switch_page("pages/Importação_&_Seleção.py")

        



with colunas[0]: 
    if st.button("Saiba Mais"):
        st.switch_page("pages/Ver_Mais.py")






#st.sidebar.markdown("<br>" * 4, unsafe_allow_html=True)


url_imagem = "https://raw.githubusercontent.com/BioAssis/BAS/main/BAS/midias/logo.jpeg"

st.sidebar.image(url_imagem, use_column_width=True)