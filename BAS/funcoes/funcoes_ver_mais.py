import pandas as pd
import numpy as np
import copy
import streamlit as st # type: ignore
import funcoes.funcoes_gerais as fn


def iniciar_ver_mais():

    # Sobre o Projeto
    st.write("""
    Information on this page has been omitted.
    """)

    st.markdown("<br>" * 4, unsafe_allow_html=True)
    colunas = st.columns(4)

    
    with colunas[3]: 
        if st.button("Página Inicial"):
            st.switch_page("Pagina_Inicial.py")

