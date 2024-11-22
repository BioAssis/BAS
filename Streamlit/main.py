#Importar as bibliotecas
import pandas as pd
import streamlit as st   # type: ignore
import funcoes_bas as fbas
import copy
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode   # type: ignore


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
                df_importado = pd.read_excel(uploaded_file, engine="openpyxl", header=None)
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


        df_tabela = fbas.gerar_tabela(dici_final, poços_selecionados)




        if poços_selecionados == None:
            poços_selecionados = fn.seleciona_da_tabela(df_tabela)

        

        


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
            fbas.gerar_tres_graficos(df_dict_com_triplicata,poços_selecionados)

        else:
            st.markdown("Nenhum poço selecionado.")
















    with compare:
        if poços_selecionados is not None and len(poços_selecionados) > 0:

            #st.write("Conteúdo para comparação:", poços_selecionados)


            #st.write("Defina as opções de seu gráfico:")

            #st.write(df_para_graficos)

            modelo_escolhido = st.selectbox(
                'Modelos Possíveis',
                ["Gompertz", "Zwietering", "Linear", "Exponencial"],  
                index=0
            )


            if modelo_escolhido == "Gompertz":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = int(st.number_input("Insira o primeiro valor:", value=0.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = int(st.number_input("Insira o segundo valor:", value=30.0, format="%.2f", step=0.5)) 

            elif modelo_escolhido == "Zwietering":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = int(st.number_input("Insira o primeiro valor:", value=0.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = int(st.number_input("Insira o segundo valor:", value=30.0, format="%.2f", step=0.5)) 
            
            elif modelo_escolhido == "Linear":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = int(st.number_input("Insira o primeiro valor:", value=5.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = int(st.number_input("Insira o segundo valor:", value=12.0, format="%.2f", step=0.5)) 
            
            elif modelo_escolhido == "Exponencial":
                colunas = st.columns(2)

                with colunas[0]:
                    ini_log = int(st.number_input("Insira o primeiro valor:", value=5.0, format="%.2f", step=0.5))
                        
                with colunas[1]:     
                    fim_log = int(st.number_input("Insira o segundo valor:", value=12.0,format="%.2f", step=0.5)) 

            else:
                ini_log = 0      
                fim_log = 0
            

             
            if modelo_escolhido == "Linear":
                df_tabela_final = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_escolhido, ini_log, fim_log)
                

            elif modelo_escolhido == "Exponencial":
                df_tabela_final = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_escolhido, ini_log, fim_log)


            else:
                df_tabela_final = fbas.gerar_tabela(dici_final,poços_selecionados, modelo_escolhido, ini_log, fim_log)
        


            df_sem_triplicata_com_std = fbas.gerar_df_com_std(dici_final, df_dict_com_triplicata, poços_selecionados, modelo_escolhido) # IMPORTANTE !!!!!!!
           





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


                legendas_padrao = fbas.gerar_legendas(df_tabela_final)

                
                legendas = []

                
                opcao_legenda = st.selectbox(
                    'Legendas',
                    ["Padrão", "Manual"],  # Opções
                    index=0
                )

                if opcao_legenda == "Padrão":
                    legendas = legendas_padrao


                else:
                    colunas = st.columns(2)

                    terco = len(legendas_padrao) // 2 
                    excesso = len(legendas_padrao) % 2  # Excesso de elementos ao dividir por 3


                    # Coloca os valores em cada coluna, considerando o excesso
                    with colunas[0]:
                        for col in legendas_padrao[0:terco + (1 if excesso > 0 else 0)]:
                            legenda = st.text_input(f"Legenda: {col}", value=col)
                            legendas.append(legenda)


                    with colunas[1]:
                        for col in legendas_padrao[terco + (1 if excesso > 0 else 0):]:
                            legenda = st.text_input(f"Legenda: {col}", value=col)
                            legendas.append(legenda)

            
            fbas.plota_dataset_selecionado_final(df_sem_triplicata_com_std, poços_selecionados, titulo, xlabel, ylabel, legendas, fonte_selecionada, tamanho_legenda, tamanho_titulo)


            
            if st.button("Gerar Tabela"):

                teste = pd.DataFrame(df_tabela_final)

                
                st.write(teste)
        



        else:
            st.markdown("Nenhum poço selecionado.")


else:
    st.write("Importe um arquivo antes de continuar")

# "importar" -> "artquivo to placa" -> ""
