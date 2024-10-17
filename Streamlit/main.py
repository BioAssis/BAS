#Importar as bibliotecas
import numpy as np
import pandas as pd
import streamlit as st
from faker import Faker
import funcoes_bas as fbas
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode




#Criar as funções de carregamentos de dados

#Preparar as visualizaçôes


#Criar a interface do stram
st.write("""
# Bioprocess Assistant Software
Um app desenvolvido pelos alunos da Ilum Escola de Ciencias voltada para o suporte de aplicações biológicas
  
""")
  

select, compare = st.tabs(["Seleção de Poços", "Comparação de Poços selecionadas"])


with select:
    st.header("Todos os Poços")

    df_dict = {
    "Placa": [
        "Placa_1", "Placa_2", "Placa_3", "Placa_4", "Placa_5", "Placa_6", "Placa_7", "Placa_8", "Placa_9", "Placa_10",
        "Placa_11", "Placa_12", "Placa_13", "Placa_14", "Placa_15", "Placa_16", "Placa_17", "Placa_18", "Placa_19", "Placa_20"
    ],
    "Poço": [
        "Poço-A(1-3)", "Poço-A(1-3)", "Poço-B(1-3)", "Poço-B(1-3)", "Poço-C(1-3)", "Poço-C(1-3)", "Poço-D(1-3)", "Poço-D(1-3)", 
        "Poço-E(1-3)", "Poço-E(1-3)", "Poço-F(1-3)", "Poço-F(1-3)", "Poço-G(1-3)", "Poço-G(1-3)", "Poço-H(1-3)", "Poço-H(1-3)", 
        "Poço-I(1-3)", "Poço-I(1-3)", "Poço-J(1-3)", "Poço-J(1-3)"
    ],
    "K": [
        0.05, 0.11, 0.08, 0.09, 0.07, 0.06, 0.12, 0.13, 0.04, 0.10,
        0.14, 0.15, 0.03, 0.09, 0.08, 0.05, 0.11, 0.07, 0.06, 0.13
    ],
    "Tlag": [
        20.14, 17.21, 18.45, 19.10, 21.32, 20.87, 16.95, 17.45, 18.23, 19.65,
        15.23, 14.78, 19.32, 18.11, 21.54, 20.09, 17.98, 16.57, 22.15, 18.67
    ],
    "Nmax": [
        8.52, 12.56, 10.23, 11.45, 9.87, 10.56, 12.23, 13.14, 8.95, 11.32,
        9.42, 10.78, 8.65, 12.01, 11.92, 10.11, 13.21, 9.85, 10.65, 11.47
    ],
    "Growth Score": [
        7.12, 6.33, 6.87, 7.45, 6.98, 7.01, 6.12, 7.32, 6.76, 7.89,
        6.54, 7.15, 6.22, 7.36, 7.01, 6.44, 7.25, 6.91, 6.33, 7.52
    ]
}

# Convertendo o dicionário em um DataFrame
    df = pd.DataFrame(df_dict)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()


    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
    )

    selected_rows = grid_response["selected_rows"]  # Pega as linhas selecionadas


    st.header("Poços Selecionados")
    if selected_rows is not None and len(selected_rows) > 0:

        filtered_df = pd.DataFrame(selected_rows)
        st.write(selected_rows) 
    else:
        st.markdown("NNenhum poço selecionado ")

with compare:
    if selected_rows is not None and len(selected_rows) > 0:
        st.write("Conteúdo para comparação:", selected_rows)

        # Verifique o tipo de selected_rows antes de tentar acessar
        if isinstance(selected_rows, list) and len(selected_rows) > 0:
            # Caso selected_rows seja uma lista de dicionários
            try:
                if isinstance(selected_rows[0], dict):
                    selected_names = [row['name'] for row in selected_rows]

                    # Prepare os dados para atividade e atividade diária
                    activity_df = {name: row['activity'] for name, row in zip(selected_names, selected_rows)}
                    activity_df = pd.DataFrame(activity_df)

                    daily_activity_df = {name: row['daily_activity'] for name, row in zip(selected_names, selected_rows)}
                    daily_activity_df = pd.DataFrame(daily_activity_df)

                    st.header("Daily activity comparison")
                    st.bar_chart(daily_activity_df)

                    st.header("Yearly activity comparison")
                    st.line_chart(activity_df)
                else:
                    pass  # Ignora se não for uma lista de dicionários
            except KeyError:
                pass  # Ignora o KeyError

    else:
        st.markdown("No members selected.")