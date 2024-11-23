import pandas as pd
import numpy as np
import copy
import streamlit as st # type: ignore
import funcoes.funcoes_gerais as fn



def iniciar_tratamento_plotagem():

    
    if st.session_state.poços_selecionados is not None and len(st.session_state.poços_selecionados) > 0: 

        poços_selecionados = st.session_state.poços_selecionados  # Definindo cada uma dessas variáveis atravez da função.
        dici_final = copy.deepcopy(st.session_state.dici_final)   # Definindo cada uma dessas variáveis atravez da função.
        dici_final_com_triplicatas = st.session_state.dici_final_com_triplicatas   # Definindo cada uma dessas variáveis atravez da função.
            
        modelo_escolhido, ini_log, fim_log = fn.escolher_modelo() # Definindo cada uma dessas variáveis atravez da função. 
            
        
        df_tabela_final = fn.gerar_tabela(dici_final,poços_selecionados, modelo_escolhido, ini_log, fim_log)  #Tabela mostrada quando clicado em mostrar tabela, literalmente a tabela final.
    
        df_sem_triplicata_com_std = fn.gerar_df_com_std(dici_final, dici_final_com_triplicatas, poços_selecionados, modelo_escolhido) # IMPORTANTE !!!!!!!


    
        fn.gerar_grafico_final(df_sem_triplicata_com_std, poços_selecionados, df_tabela_final, ini_log,fim_log)

    



        
        colunas = st.columns(4)

        with colunas[0]:
            if st.button("Voltar para Seleção"):
                st.switch_page("pages/Importação_&_Seleção.py")



        with colunas[3]:
            if st.button("Saiba Mais Sobre o Projeto"):
                st.switch_page("pages/Ver_Mais.py")
        
    else: 
        st.write("Nenhum poço foi selecionado ainda. Volte para a seção anterior e selecione os poços de seu interesse.")


        colunas = st.columns(4)

        st.markdown("<br>" * 3, unsafe_allow_html=True)

        with colunas[0]:

            if st.button("Selecionar dados"):

                st.switch_page("pages/Importação_&_Seleção.py")



        with colunas[3]:
            if st.button("Saiba Mais Sobre o Projeto"):
                st.switch_page("pages/Ver_Mais.py")