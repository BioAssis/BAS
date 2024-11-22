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


    dados_brutos = fn.importar_arquivos()
    if len(dados_brutos) != 0:

            
        df_dict_com_triplicata, df_dict_sem_triplicata = fn.arquivos_to_placas(dados_brutos)  # Gera os 2 dfs, com e sem triplicata.

        
        dici_final = copy.deepcopy(df_dict_sem_triplicata) # Copia o df para não alterar o arquivo fonte


        poços_selecionados = None


        df_tabela = fn.gerar_tabela(dici_final, poços_selecionados) # A partir de dici_final(sem_triplicatas) cria uma tabela com os parametros de cada poço.


        
        poços_selecionados = fn.seleciona_da_tabela(df_tabela) # Caso não exista poço selecionado cria a grid de seleção.


        
        if poços_selecionados is not None and len(poços_selecionados) > 0:
            st.header("Poços Selecionados")
            st.write(poços_selecionados)



            st.header("Análise individual:")
            fn.gerar_tres_graficos(df_dict_com_triplicata,poços_selecionados)




        # Inicializa as variáveis no session_state na primeira execução

        if 'botton_print' not in st.session_state:
            st.session_state['botton_print'] = False  # Começa desligado
            
        if 'a' not in st.session_state:
            st.session_state['a'] = []
            # Inicializa como None





        st.session_state['botton_print'] = not st.session_state['botton_print']

        if st.session_state['botton_print']:
            st.session_state['dici_final'] = dici_final
            st.session_state['poços'] = poços_selecionados    

        else:
            st.write("Nenhum poço selecioando ainda.")

        
    else:
        st.write("Selecione um arquivo clicando logo acima.")    




