#Importar as bibliotecas
import numpy as np
import pandas as pd
import streamlit as st
from faker import Faker
from lmfit import Model
import funcoes_bas as fbas
import seaborn as sns
import copy
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import Legend, LegendItem
from bokeh.palettes import Dark2
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode


st.set_page_config(layout="wide")

#Criar as funções de carregamentos de dados

#Preparar as visualizaçôes


#Criar a interface do stram
st.write("""
# Bioprocess Assistant Software
Um app desenvolvido pelos alunos da Ilum Escola de Ciencias com enfoque em  aplicações biológicas.
  
""")
  

st.sidebar.markdown(
    "<h1 style='font-size:24px;'>Selecione os arquivos</h1>", 
    unsafe_allow_html=True
)



# ----------------------------------- Importando dados e os Organizando ----------------------------------

uploaded_files = st.sidebar.file_uploader(
    " ", 
    type=["xlsx", "csv", "txt"], 
    accept_multiple_files=True, 
    key="import"
)

dados_brutos = []

if uploaded_files:
    arquivos = 0
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                arquivos += 1

            elif uploaded_file.name.endswith(".xlsx"):
                df_importado = pd.read_excel(uploaded_file, engine="openpyxl")
                dados_brutos.append(df_importado)
                arquivos += 1
                

            elif uploaded_file.name.endswith(".txt"):
                content = uploaded_file.read().decode("utf-8")
                arquivos += 1

        except Exception as e:
            st.error(f"Erro ao ler {uploaded_file.name}: {str(e)}")

    st.sidebar.write(f"{arquivos} arquivos foram carregados.")
                #st.dataframe(df)


#-------------------------------------------------------------------------------------------------------------------------------------


select, compare = st.tabs(["Seleção de Poços", "Comparação de Poços selecionadas"])

if uploaded_files:
    with select:
        st.header("Todos os Poços")

        df_dict_com_triplicata, df_dict_sem_triplicata = fbas.arquivos_to_placas(dados_brutos)

        dici_final = copy.deepcopy(df_dict_sem_triplicata)

        poços_selecionados = None

        df_tabela, algo_1 = fbas.gerar_tabela(dici_final, poços_selecionados)



        def seleciona_da_tabela(df_tabela):
            # Descrição de Cada Coluna do dataset
            column_tooltips = {
            "Placa": "Identificação da placa.",
            "Poço": "Identificação do poço.",
            "μMax": "Taxa de crescimento dos micro-organismos.",
            "Fase lag": "Tempo de adaptação antes do crescimento exponencial.",
            "A": "População máxima de micro-organismos.",
            "Growth Score": "Pontuação de crescimento calculada."
            }

            # Certifique-se de que o dataframe não tenha colunas duplicadas
            df = pd.DataFrame(df_tabela).drop_duplicates()

            # Configurando GridOptions com tooltip
            gb = GridOptionsBuilder.from_dataframe(df)

            # Adicionando descrições para cada coluna
            for col, tooltip in column_tooltips.items():
                if col in df.columns:
                    gb.configure_column(col, headerTooltip=tooltip)

            # Configuração de seleção e grid
            gb.configure_selection(selection_mode="multiple", use_checkbox=True)
            grid_options = gb.build()

            # Exibindo o AgGrid com as configurações ajustadas
            grid_response = AgGrid(
                df,
                gridOptions=grid_options,
                data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                update_mode=GridUpdateMode.MODEL_CHANGED,
                fit_columns_on_grid_load=True,
                theme='streamlit',  # Altere para um dos temas válidos
            )

            
            # Capturando as linhas selecionadas
            poços_selecionados = grid_response.get("selected_rows", [])  # Evita erros se não houver seleções
        
            return poços_selecionados


        if poços_selecionados == None:
            poços_selecionados = seleciona_da_tabela(df_tabela)
        



        st.header("Poços Selecionados")
        if poços_selecionados is not None and len(poços_selecionados) > 0:

            filtered_df = pd.DataFrame(poços_selecionados)
            #st.dataframe(selected_rows.reset_index(drop=True))
            st.write(filtered_df)

            modelo = "Gompertz"

            #teste = fbas.modela_selecionados(dici_final,filtered_df,modelo)
            #df_final = pd.DataFrame(teste)    

            

        # ----------------------------------------------------------------------
            st.header("Análise individual:")
            fbas.gera_tres_graficos(df_dict_com_triplicata,poços_selecionados)

        else:
            st.markdown("Nenhum poço selecionado.")




    with compare:
        if poços_selecionados is not None and len(poços_selecionados) > 0:

            #st.write("Conteúdo para comparação:", poços_selecionados)


            #st.write("Defina as opções de seu gráfico:")

            #st.write(df_para_graficos)

            modelo_usado = st.selectbox(
                'Modelos Possíveis',
                ["Gompertz", "Zwietering", "Linear", "Exponencial"],  
                index=0
            )
    
            
            if modelo_usado == "Linear":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = 2 * int(st.number_input("Insira o primeiro valor:", value=5.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = 2 * int(st.number_input("Insira o segundo valor:", value=12.0, format="%.2f", step=0.5)) 
            
            elif modelo_usado == "Exponencial":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = int(st.number_input("Insira o primeiro valor:", value=5.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = int(st.number_input("Insira o segundo valor:", value=12.0,format="%.2f", step=0.5)) 

            else:
                ini_log = 0      
                fim_log = 0
            


            st.write("Teste")
            
            if modelo_usado == "Linear":
                df_tabela_final = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_usado, ini_log, fim_log)
                

            elif modelo_usado == "Exponencial":
                df_tabela_final = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_usado, ini_log, fim_log)


            else:
                df_tabela_final, df_com_previsoes = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_usado, ini_log, fim_log)
                df_seila = fbas.filtra_dataset(df_com_previsoes, poços_selecionados)  # Devolve o dataset original porem só com os poços selecionados com as previsões.

            
            teste = pd.DataFrame(df_tabela_final)

               
            st.write(teste)






            df_para_graficos = fbas.cria_dataset_grafico(dici_final, poços_selecionados, modelo_usado) # Existe só pra não da erro em todo o resto

             




            with st.expander("Opções de edição do Gráfico"):
                st.write("Aqui está um exemplo de um gráfico:")
                colunas = st.columns(3)

                with colunas[0]:
                    xlabel = st.text_input('Rótulo do Eixo X', 'Tempo (horas)') 
                    ylabel = st.text_input('Rótulo do Eixo Y', 'Green Value')

                with colunas[1]:
                    titulo = st.text_input('Título do Gráfico', 'Crescimento Médio(Green Value x Tempo)')
                    fonte_selecionada = st.selectbox(
                        "Escolha a fonte do gráfico:",
                        ["Arial", "Times New Roman", "Helvetica"]
                    )

                with colunas[2]:
                    tamanho_legenda = st.number_input("Tamanho da legenda", value=12, step=1)
                    tamanho_titulo = st.number_input("Tamanho do titulo", value=14, step=1)

                legendas = []

                
                opcao_legenda = st.selectbox(
                    'Legendas',
                    ["Padrão", "Manual"],  # Opções
                    index=0
                )

                if opcao_legenda == "Padrão":
                    legendas = df_para_graficos.columns[1:]

                else:
                    colunas = st.columns(3)

                    terco = len(df_para_graficos.columns) // 3 

                    with colunas[0]:
                        for col in df_para_graficos.columns[1:terco+1]:
                            legenda = st.text_input(f"Legenda: {col}", value=col)
                            legendas.append(legenda)

                    with colunas[1]:
                        for col in df_para_graficos.columns[terco+1:(2*terco)+1]:
                            legenda = st.text_input(f"Legenda: {col}", value=col)
                            legendas.append(legenda)

                    with colunas[2]:
                        for col in df_para_graficos.columns[2*terco+1:]:
                            legenda = st.text_input(f"Legenda: {col}", value=col)
                            legendas.append(legenda)


            df_teste = fbas.cria_dataset_grafico(dici_final, poços_selecionados, modelo_usado)
            
            
            if modelo_usado == "Linear":
                fbas.plota_dataset_selecionado_para_linear(df_teste, titulo, xlabel, ylabel, legendas, fonte_selecionada, tamanho_legenda, tamanho_titulo)

                
            elif modelo_usado == "Exponencial":
                fbas.plota_dataset_selecionado_para_linear(df_tabela_final, titulo, xlabel, ylabel, legendas, fonte_selecionada, tamanho_legenda, tamanho_titulo)

            else:

                fbas.plota_dataset_selecionado_padrao(df_seila, titulo, xlabel, ylabel, legendas, fonte_selecionada, tamanho_legenda, tamanho_titulo)
            

            

        else:
            st.markdown("Nenhum poço selecionado.")


else:
    st.write("Importe um arquivo antes de continuar")

# "importar" -> "artquivo to placa" -> ""
