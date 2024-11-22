import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
from lmfit import Model
import streamlit as st # type: ignore
from bokeh.plotting import figure  # type: ignore
from bokeh.palettes import Dark2   # type: ignore
from bokeh.models import ColumnDataSource, Legend, LegendItem, HoverTool   # type: ignore
from bokeh.models import Whisker   # type: ignore

import funcoes.funcoes_gerais as fn



def importar_e_selecionar():

    

    if 'dados_salvos' not in st.session_state:
        dados_brutos = fn.importar_arquivos()

    else:
        dados_salvos = copy.deepcopy(st.session_state.dados_salvos)
        dados_atuais = fn.importar_arquivos()

        dados_brutos = dados_salvos + dados_atuais


    

    if len(dados_brutos) != 0:

        st.markdown("<br>" * 2, unsafe_allow_html=True)
            
        df_dict_com_triplicata, df_dict_sem_triplicata = fn.arquivos_to_placas(dados_brutos)  # Gera os 2 dfs, com e sem triplicata.

        dici_final = copy.deepcopy(df_dict_sem_triplicata) # Copia o df-sem-triplicata para não alterar o arquivo fonte
        dici_final_com_triplicatas = copy.deepcopy(df_dict_com_triplicata) # Copia o df-com-triplicata para não alterar o arquivo fonte

        poços_selecionados = None


        df_tabela = fn.gerar_tabela(dici_final, poços_selecionados) # A partir de dici_final(sem_triplicatas) cria uma tabela com os parametros de cada poço.


        
        poços_selecionados = fn.seleciona_da_tabela(df_tabela) # Caso não exista poço selecionado cria a grid de seleção.


        st.header("Poços Selecionados")

        if poços_selecionados is not None and len(poços_selecionados) > 0:

            st.write(poços_selecionados)


            st.header("Análise individual:")
            fn.gerar_tres_graficos(dici_final_com_triplicatas,poços_selecionados)

        else:
            st.write("Nenhum poço selecionado até o momento.")

        


        st.markdown("<br>" * 1, unsafe_allow_html=True)


        colunas = st.columns(4)

        with colunas[3]:

            if st.button("Tratamento de Dados"):

                st.session_state.dici_final = dici_final  #Criando o session_state dici_final 

                st.session_state.dici_final_com_triplicatas = dici_final_com_triplicatas #Criando o session_state dici_final_com_triplicatas.

                st.session_state.poços_selecionados = poços_selecionados #Criando o session_state poços_selecio

                st.session_state.dados_salvos = dados_brutos #Criando o session_state poços_selecionados

                st.switch_page("pages/Tratamento_&_Plotagem.py")
        
        
    else:
        st.write("Selecione um arquivo clicando logo acima.")   


    




