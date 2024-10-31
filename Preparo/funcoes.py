import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import streamlit as st # type: ignore
import seaborn as sns
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Dark2
from bokeh.models import ColumnDataSource, LineEditTool, Legend, LegendItem


#______________________________________________________________________________________________________________________________________________


def organizacao_e_separacao_triplicatas(dataset):
    """
    Processa um dataset de experimentos com triplicatas, calculando a média das triplicatas e transformando a primeira 
    coluna de tempo de minutos para horas. Retorna dois DataFrames:
    1. Um com o tempo convertido e as triplicatas lado a lado.
    2. Outro com as médias das triplicatas e o tempo convertido.
    

    Args:
        dataset: DataFrame do pandas contendo os dados experimentais. 
    
    Returns: 
        tuple:
            - DataFrame com a primeira coluna sendo o tempo em horas, e as colunas das triplicatas substituídas pelas médias.
            - DataFrame com a primeira coluna sendo o tempo em horas, e as triplicatas lado a lado.
    """

    # DataFrame para as médias
    dataset_sem_triplicatas = pd.DataFrame(dataset.iloc[:, 0])  # Reservando a primeira coluna do dataset (tempo em minutos)
    dataset_sem_triplicatas.columns = ['Tempo(horas)']

    # Converter o tempo de minutos para horas
    dataset_sem_triplicatas["Tempo(horas)"] = dataset_sem_triplicatas["Tempo(horas)"] / 60

    # Número de colunas de dados (excluindo a primeira coluna de tempo)
    colunas_real = int(len(dataset.columns) - 1)

    letras_colunas = ["A", "B", "C", "D", "E", "F", "G", "H"]

    # DataFrame para as triplicatas lado a lado
    dataset_com_triplicatas = pd.DataFrame(dataset.iloc[:, 0])  # Reservando a primeira coluna do dataset (tempo em minutos)
    dataset_com_triplicatas.columns = ['Tempo(horas)']
    dataset_com_triplicatas["Tempo(horas)"] = dataset_com_triplicatas["Tempo(horas)"] / 60


    colunas = colunas_real // 3

    letra = 0
    passo = 1

    for i in range(1, colunas+1):
        colunas_para_media = dataset.iloc[:, (i*3 - 2):(i*3 + 1)]  # Colunas das triplicatas

        # Calcula a média das três colunas para cada linha
        media_colunas = colunas_para_media.mean(axis=1)

        # Adiciona a coluna de médias no dataset de médias
        dataset_sem_triplicatas[f'Poço_{letras_colunas[letra]}({(passo*3-2)}-{(passo*3)})'] = media_colunas

        if (i % 4) == 0:
            letra += 1
        
        if passo == 4:
            passo = 1
        else:
            passo += 1


    letra = 0
    passo = 1

    for i in range(1, colunas_real+1):

        dataset_com_triplicatas[f"Poço_{letras_colunas[letra]}({passo})"] = dataset.iloc[:,i]

        if (i % 12) == 0 :
            letra += 1

        if passo == 12:
            passo = 1
        else:
            passo += 1


    return  dataset_com_triplicatas, dataset_sem_triplicatas

#____________________________________________________________________________________________________________________


def construir_dici_poços(dataset_triplicatas, dataset_sem_triplicatas):
    """
    Função que constrói dois dicionários de datasets a partir de dois datasets diferentes:
    
    1. Para `dataset_triplicatas`: 
       - As chaves seguem o padrão "Poço_X(n-(n+3))", onde X é uma letra (A, B, C...) e n é o índice da primeira triplicata.
       - As colunas das triplicatas são renomeadas para o formato "Poço_A(1)", "Poço_A(2)", "Poço_A(3)", etc.
       
    2. Para `dataset_sem_triplicatas`:
       - As chaves são os nomes das colunas dos poços.
       - As colunas são renomeadas para "Tempo(horas)" e "y_experimental".
    
    Args:
        dataset_triplicatas: DataFrame contendo as triplicatas lado a lado.
        dataset_sem_triplicatas: DataFrame com os dados experimentais a serem renomeados.

    Returns:
        tuple: Dois dicionários
            - dicionário 1: Com as triplicatas renomeadas.
            - dicionário 2: Com as colunas renomeadas para "Tempo(horas)" e "y_experimental".
    """
    
    # Dicionário 1: Para dataset_triplicatas
    dici_triplicatas = {}
    tempo_coluna = dataset_triplicatas.columns[0]  # Primeira coluna "Tempo(horas)"
    
    num_colunas_poço = 3  # Número de colunas por triplicata (A_1, A_2, A_3, etc.)
    letras_colunas = ["A", "B", "C", "D", "E", "F", "G", "H"]

    for letra_idx, letra in enumerate(letras_colunas):
        for i in range(0, 12, num_colunas_poço):
            # Nome da chave no formato "Poço_X(n-m)"
            chave = f"Poço_{letra}({i+1}-{i+num_colunas_poço})"

            # Pegando a coluna "Tempo(horas)" e as 3 colunas consecutivas do poço
            colunas_poço = [tempo_coluna] + [f"Poço_{letra}({i+j+1})" for j in range(num_colunas_poço)]
            dici_triplicatas[chave] = dataset_triplicatas[colunas_poço]

    # Dicionário 2: Para dataset_sem_triplicatas
    primeira_coluna = dataset_sem_triplicatas.columns[0]
    dici_sem_triplicatas = {
        col: dataset_sem_triplicatas[[primeira_coluna, col]].rename(columns={col: "y_experimental"})
        for col in dataset_sem_triplicatas.columns[1:]
    }
    # Retorna os dois dicionários
    return dici_triplicatas, dici_sem_triplicatas
#__________________________________________________________________________________________________________________


def construir_dici_placas(arquivos):
    """
    Essa função vai recerber uma lista de com dicionários e a partir dessa lista, criar um novo dicionario,
    em que cada dicionário da lista anterior, pode ser chamado através da chave 
    "Placa_{(indice do dicionario na lista) + 1}".

    arquivos: Lista de dicionários
    
    :return: Dicionário, onde cada chave segue o formato 'Placa_{i}' e
             o valor correspondente é o dicionário de poços respectivo.
    """

    dici_placas = {}
    for i, dic in enumerate(arquivos, start=1):
        # Cria a chave "Placa_{i}" e atribui o dicionário de poços
        dici_placas[f"Placa_{i}"] = dic
    
    return dici_placas

#____________________________________________________________________________________________________________________


def arquivos_to_placas(dados_brutos):
    """
    Constrói um dicionário de placas a partir de uma lista de dicionários de poços.

    Args:
        arquivos: Lista de dicionários de poços.

    return: 
        Dicionário de placas organizado.
    """

    
    lista_df_destriplicados = []
    lista_df_triplicados = []  # É preciso passar pela função pois ela organiza os dados.

    for dados in dados_brutos: 

        df_com_triplicatas, df_sem_triplicatas = organizacao_e_separacao_triplicatas(dados)  # Pegando apenas o DataFrame

        lista_df_destriplicados.append(df_sem_triplicatas)
        lista_df_triplicados.append(df_com_triplicatas)

    lista_dici_poços_sem_triplicatas = []
    lista_dici_poços_com_triplicatas = []

    # Preencher as listas de dicionários diretamente com os DataFrames processados
    for i in range(len(lista_df_triplicados)):
        dici_poços_com_triplicatas, dici_poços_sem_triplicatas = construir_dici_poços(lista_df_triplicados[i], lista_df_destriplicados[i])
        lista_dici_poços_com_triplicatas.append(dici_poços_com_triplicatas)
        lista_dici_poços_sem_triplicatas.append(dici_poços_sem_triplicatas)

    # Construir o dicionário de placas
    dici_placas_com_triplicatas = construir_dici_placas(lista_dici_poços_com_triplicatas)
    dici_placas_sem_triplicatas = construir_dici_placas(lista_dici_poços_sem_triplicatas)

    return dici_placas_com_triplicatas, dici_placas_sem_triplicatas



#-------------------------------------- Funções Matemáticas para Modelagem dos Crescimentos ------------------------------------------------

def gompertz(t, Nmax, k, tlag):
    '''
    Calcula a função de Gompertz para modelar o crescimento microbiano.

    Args:
        t (float): Tempo em unidades de horas.
        Nmax (float): Valor assintótico máximo da população de micro-organismos. Representa a capacidade máxima de crescimento da cultura.
        k (float): Taxa de crescimento específica. Determina a rapidez com que a população de micro-organismos cresce após o período de lag.
        tlag (float): Tempo de lag ou atraso antes do início do crescimento exponencial. Representa o tempo necessário para a adaptação inicial da população.

    Returns:
        float: Resultado da função de Gompertz, o valor estimado da população de micro-organismos para cada instante de tempo.
    '''
    return Nmax * np.exp(-np.exp(-k * (t - tlag)))


def zwietering(t, y_0, Nmax, k, tlag):
    """
    Calcula a função modificada de Gompertz para modelar o crescimento microbiano.

    A função de Gompertz é frequentemente usada para descrever o crescimento de populações biológicas, como o crescimento microbiano, com base em parâmetros que controlam a taxa de crescimento, o tempo de atraso (lag) e o valor máximo de crescimento.

    Args:
        t (float): Tempo em unidades de horas.
        y_0 (float): Valor inicial da variável de resposta no tempo zero (t=0).
        Nmax (float): Amplitude do crescimento ou valor assintótico máximo atingido pela função.
        k (float): Taxa de crescimento específica, controlando a rapidez com que o crescimento ocorre após o período de lag.
        tlag (float): Tempo de lag ou atraso, representando o tempo necessário para a adaptação inicial antes do crescimento exponencial.

    Returns:
        float: O valor estimado da função de Gompertz no tempo `t`, representando o crescimento da população microbiana ao longo do tempo.
    """
    return y_0 + ((Nmax - y_0)/(1 + np.exp(((4 * k)/Nmax) * (tlag - t) + 2)))

def linear(t, slope, intercept):
    """Define uma função linear que será usada para o ajuste de dados.
    
    Args:
        t (float): Tempo em unidades de horas.
        slope (float): Também chamado de coeficiente angular é angulo de inclinação da reta.
        intercept (float): Valor onde a reta atravessa o eixo y

    Returns:
        float: O valor estimado da modelagem linearno tempo `t`, representando o crescimento da população microbiana ao longo do tempo.
    """
    return slope * t + intercept

def exponencial(t, Nmax, k):
    """Função que recebe um tempo(t) e apartir dele e da taxa de crescimento da determinada população ele calcula um valor a partir de uma equação exponencial.
    
    Args:
        t (float): Tempo em unidades de horas.
        Nmax (float): Amplitude do crescimento ou valor assintótico máximo atingido pela função.
        k (float): Taxa de crescimento específica, controlando a rapidez com que o crescimento ocorre após o período de lag.

    Returns:
        float: O valor estimado de uma função Exponencial no tempo "t", representando o crescimento da população microbiana ao longo do tempo.
    """
    
    return Nmax * np.exp(k * t)



#------------------------------------------ Calculando Growth Score -----------------------------------------------


def growth_score(k, Nmax, y_0 = 0):
    """
    Calcula a pontuação de crescimento com base na taxa de crescimento específica (k) e nos valores assintóticos da população.

    Args:
        k (float): Taxa de crescimento específica. Representa a rapidez com que a população de micro-organismos cresce.
        Nmax (float): Valor assintótico máximo da população de micro-organismos. Representa a capacidade máxima de crescimento.
        y_0 (float): Valor inicial da população de micro-organismos.

    Returns:
        float: Pontuação de crescimento, calculada como a diferença entre o valor máximo e o valor inicial da população acrescida de 25% da taxa de crescimento.
    """
    return (Nmax - y_0) + 0.25*k


#------------------------------------------ Gerando Tabela ----------------------------------------------------



def gerar_tabela(dici_final,df_selecionados, modelo_escolhido = "Gompertz", ini_log = 0, fim_log = 0):
    """ Essa função recebe 5 parametros, e devolve um dicionario comtendo os parametros específicos do cresciemnto populacional de cada poço especificado 
    pela variável df_selecionados.

    Args:
        dici_final (dataset): Dataset geral com as médias das triplicatas já calculadas.
        df_selecionados (dataset): Dataset dos poços selecionados previamente. 
        modelo_escolhido (str): Uma string que define qual o modelo será usado para modelar os dados de dici_final.
        ini_log (int): Um valor que destrescreve o ponto inical da fase log, usado e necessario quando utilizados os modelos Linear e Exponencial. 
        fim_log (int, optional): _description_. Defaults to 0.

    Returns:
        dicionario: Dicionário que recebe os parametros das curvas fitadas para o crescimento de cada um dos poços selecionados pelo usuário. 
    """

    tabela = {
            "Placa": [],
            "Poços": [],
            "R²": [],
            "μMax": [],
            "A": [],
            "Fase lag": [],
            "Growth Score": [],
            }


    if modelo_escolhido == "Gompertz":
        
        if df_selecionados is None:
            for placa in dici_final:
                for poço in dici_final[placa]:

                    x = dici_final[placa][poço]["Tempo(horas)"]
                    y = dici_final[placa][poço]["y_experimental"]
                    
                    modelo_gompertz = Model(gompertz)

                    params = modelo_gompertz.make_params(Nmax=10, k=0.5, tlag=1)
                    params['Nmax'].min = 0  # Limite mínimo para A
                    params['k'].min = 0.01  # Limite mínimo para μMax
                    params['tlag'].min = 0  # Limite mínimo para tlag

                    resultado_fit = modelo_gompertz.fit(y, params, t=x)

                    y_predito = resultado_fit.best_fit
                    ss_total = np.sum((y - np.mean(y)) ** 2)
                    ss_residual = np.sum((y - y_predito) ** 2)
                    r2 = 1 - (ss_residual / ss_total)

                    GS = growth_score(resultado_fit.params["k"].value,resultado_fit.params["Nmax"].value)

                    tabela["Placa"].append(placa)
                    tabela["Poços"].append(poço)
                    tabela["R²"].append(r2)
                    tabela['μMax'].append(resultado_fit.params["k"].value)
                    tabela['A'].append(resultado_fit.params["Nmax"].value)
                    tabela["Fase lag"].append(resultado_fit.params["tlag"].value)
                    tabela["Growth Score"].append(GS)

            return tabela
                
        else:
            for placa, poço in zip(df_selecionados["Placa"], df_selecionados["Poços"]):
                
                x = dici_final[placa][poço]["Tempo(horas)"]
                y = dici_final[placa][poço]["y_experimental"]
                
                modelo_gompertz = Model(gompertz)

                params = modelo_gompertz.make_params(Nmax=10, k=0.5, tlag=1)
                params['Nmax'].min = 0  # Limite mínimo para A
                params['k'].min = 0.01  # Limite mínimo para μMax
                params['tlag'].min = 0  # Limite mínimo para tlag

                resultado_fit = modelo_gompertz.fit(y, params, t=x)

                y_predito = resultado_fit.best_fit
                ss_total = np.sum((y - np.mean(y)) ** 2)
                ss_residual = np.sum((y - y_predito) ** 2)
                r2 = 1 - (ss_residual / ss_total)

                GS = growth_score(resultado_fit.params["k"].value,resultado_fit.params["Nmax"].value)

                tabela["Placa"].append(placa)
                tabela["Poços"].append(poço)
                tabela["R²"].append(r2)
                tabela['μMax'].append(resultado_fit.params["k"].value)
                tabela['A'].append(resultado_fit.params["Nmax"].value)
                tabela["Fase lag"].append(resultado_fit.params["tlag"].value)
                tabela["Growth Score"].append(GS)

            return tabela
        

    if modelo_escolhido == "Zwietering":

        if df_selecionados is None:
            for placa in dici_final:
                for poço in dici_final[placa]:
                    
                    x = dici_final[placa][poço]["Tempo(horas)"]
                    y = dici_final[placa][poço]["y_experimental"]
                    
                    modelo_zwietering = Model(zwietering)

                    params = modelo_zwietering.make_params(Nmax=0.1, k=0.1, tlag=0, y_0 = 0)
                    params['Nmax'].min = 0  # Limite mínimo para Nmax  
                    params['k'].min = 0.01  # Limite mínimo para k
                    params['tlag'].min = 0  # Limite mínimo para tlag
                    params['y_0'].min = 0  # Limite mínimo para tlag
                    params['y_0'].vary = False  # Fizando y_0

                    resultado_fit = modelo_zwietering.fit(y, params, t=x)
                    
                    y_predito = resultado_fit.best_fit
                    ss_total = np.sum((y - np.mean(y)) ** 2)
                    ss_residual = np.sum((y - y_predito) ** 2)
                    r2 = 1 - (ss_residual / ss_total)

                    GS = growth_score(resultado_fit.params["k"].value,resultado_fit.params["Nmax"].value)

                    tabela["Placa"].append(placa)
                    tabela["Poços"].append(poço)
                    tabela["R²"].append(r2)
                    tabela['μMax'].append(resultado_fit.params["k"].value)
                    tabela['A'].append(resultado_fit.params["Nmax"].value)
                    tabela["Fase lag"].append(resultado_fit.params["tlag"].value)
                    tabela["Growth Score"].append(GS)
            
            return tabela
        
        else:
            for placa, poço in zip(df_selecionados["Placa"], df_selecionados["Poços"]):

                x = dici_final[placa][poço]["Tempo(horas)"]
                y = dici_final[placa][poço]["y_experimental"]
                
                modelo_zwietering = Model(zwietering)

                params = modelo_zwietering.make_params(Nmax=0.1, k=0.1, tlag=0, y_0 = 0)
                params['Nmax'].min = 0  # Limite mínimo para Nmax  
                params['k'].min = 0.01  # Limite mínimo para k
                params['tlag'].min = 0  # Limite mínimo para tlag
                params['y_0'].min = 0  # Limite mínimo para tlag
                params['y_0'].vary = False  # Fizando y_0

                resultado_fit = modelo_zwietering.fit(y, params, t=x)

                y_predito = resultado_fit.best_fit
                ss_total = np.sum((y - np.mean(y)) ** 2)
                ss_residual = np.sum((y - y_predito) ** 2)
                r2 = 1 - (ss_residual / ss_total)

                GS = growth_score(resultado_fit.params["k"].value,resultado_fit.params["Nmax"].value)

                tabela["Placa"].append(placa)
                tabela["Poços"].append(poço)
                tabela["R²"].append(r2)
                tabela['μMax'].append(resultado_fit.params["k"].value)
                tabela['A'].append(resultado_fit.params["Nmax"].value)
                tabela["Fase lag"].append(resultado_fit.params["tlag"].value)
                tabela["Growth Score"].append(GS)

            return tabela 
            
        
    if modelo_escolhido == "Linear":
         
        if df_selecionados is None:
            for placa in dici_final:
                for poço in dici_final[placa]:

                    
                    x = dici_final[placa][poço]["Tempo(horas)"]
                    y = dici_final[placa][poço]["y_experimental"]

                    modelo_linear = Model(linear)

                    log_column = np.log(y)

                    inicio_intervalo = ini_log
                    fim_intervalo = fim_log

                    # Filtrar os dados para o intervalo especificado
                    x_intervalo = x[inicio_intervalo:fim_intervalo+1]

                    st.write(x_intervalo)
                    log_column_intervalo = log_column[inicio_intervalo:fim_intervalo+1]

                    # Definir parâmetros iniciais
                    params = modelo_linear.make_params(slope=1, intercept=0)

                    # Fazer o ajuste apenas no intervalo selecionado
                    resultado_fit = modelo_linear.fit(log_column_intervalo, params, t=x_intervalo)
                    
                    A = max(y)

                    y_predito = resultado_fit.best_fit
                    ss_total = np.sum((log_column_intervalo - np.mean(log_column_intervalo)) ** 2)
                    ss_residual = np.sum((log_column_intervalo - y_predito) ** 2)
                    r2 = 1 - (ss_residual / ss_total)

                    GS = growth_score(resultado_fit.params["slope"].value,A)
                    
                    tabela["Placa"].append(placa)
                    tabela["Poços"].append(poço)
                    tabela["R²"].append(r2)
                    tabela['μMax'].append(resultado_fit.params["slope"].value)
                    tabela['A'].append(resultado_fit.params["A"].value)
                    tabela["Fase lag"].append(inicio_intervalo)
                    tabela["Growth Score"].append(GS)
            
            return tabela  

        else:
            for placa, poço in zip(df_selecionados["Placa"], df_selecionados["Poços"]):

                st.write()
                    
                x = dici_final[placa][poço]["Tempo(horas)"]
                y = dici_final[placa][poço]["y_experimental"]

                modelo_linear = Model(linear)

                log_column = np.log(y)

                inicio_intervalo = ini_log
                fim_intervalo = fim_log

                # Filtrar os dados para o intervalo especificado
                x_intervalo = x[inicio_intervalo:fim_intervalo+1]
                log_column_intervalo = log_column[inicio_intervalo:fim_intervalo+1]

                # Definir parâmetros iniciais
                params = modelo_linear.make_params(slope=1, intercept=0)

                # Fazer o ajuste apenas no intervalo selecionado
                resultado_fit = modelo_linear.fit(log_column_intervalo, params, t=x_intervalo)
                
                A = max(y)

                y_predito = resultado_fit.best_fit
                ss_total = np.sum((log_column_intervalo - np.mean(log_column_intervalo)) ** 2)
                ss_residual = np.sum((log_column_intervalo - y_predito) ** 2)
                r2 = 1 - (ss_residual / ss_total)

                GS = growth_score(resultado_fit.params["slope"].value,A)
                
                tabela["Placa"].append(placa)
                tabela["Poços"].append(poço)
                tabela["R²"].append(r2)
                tabela['μMax'].append(resultado_fit.params["slope"].value)
                tabela['A'].append(A)
                tabela["Fase lag"].append(inicio_intervalo)
                tabela["Growth Score"].append(GS)
            
            return tabela 


    if modelo_escolhido == "Exponencial":
        
        if df_selecionados is None:
            for placa in dici_final:
                for poço in dici_final[placa]:

                    
                    x = dici_final[placa][poço]["Tempo(horas)"]
                    y = dici_final[placa][poço]["y_experimental"]

                    modelo_exponencial = Model(exponencial)


                    inicio_intervalo = ini_log
                    fim_intervalo = fim_log

                    # Filtrar os dados para o intervalo especificado
                    x_intervalo = x[inicio_intervalo:fim_intervalo+1]
                    y_intervalo = y[inicio_intervalo:fim_intervalo+1]

                    # Definir parâmetros iniciais
                    params = modelo_exponencial.make_params(Nmax=0, k=0.5)

                    # Fazer o ajuste apenas no intervalo selecionado
                    resultado_fit = modelo_exponencial.fit(y_intervalo, params, t=x_intervalo)
                    
                    A = max(y)

                    y_predito = resultado_fit.best_fit
                    ss_total = np.sum((y_intervalo - np.mean(y_intervalo)) ** 2)
                    ss_residual = np.sum((y_intervalo - y_predito) ** 2)
                    r2 = 1 - (ss_residual / ss_total)

                    GS = growth_score(resultado_fit.params["k"].value,A)
                    
                    tabela["Placa"].append(placa)
                    tabela["Poços"].append(poço)
                    tabela["R²"].append(r2)
                    tabela['μMax'].append(resultado_fit.params["k"].value)
                    tabela['A'].append(A)
                    tabela["Fase lag"].append(inicio_intervalo)
                    tabela["Growth Score"].append(GS)
            
            return tabela  

        else:
            for placa, poço in zip(df_selecionados["Placa"], df_selecionados["Poços"]):

                st.write()
                    
                x = dici_final[placa][poço]["Tempo(horas)"]
                y = dici_final[placa][poço]["y_experimental"]

                modelo_exponencial = Model(exponencial)

                log_column = np.log(y)

                inicio_intervalo = ini_log
                fim_intervalo = fim_log

                # Filtrar os dados para o intervalo especificado
                x_intervalo = x[inicio_intervalo:fim_intervalo+1]
                y_intervalo = y[inicio_intervalo:fim_intervalo+1]

                # Definir parâmetros iniciais
                params = modelo_exponencial.make_params(Nmax=0, k=0.5)

                # Fazer o ajuste apenas no intervalo selecionado
                resultado_fit = modelo_exponencial.fit(y_intervalo, params, t=x_intervalo)
                
                A = max(y)

                y_predito = resultado_fit.best_fit
                ss_total = np.sum((y_intervalo - np.mean(y_intervalo)) ** 2)
                ss_residual = np.sum((y_intervalo - y_predito) ** 2)
                r2 = 1 - (ss_residual / ss_total)

                GS = growth_score(resultado_fit.params["k"].value,A)
                
                tabela["Placa"].append(placa)
                tabela["Poços"].append(poço)
                tabela["R²"].append(r2)
                tabela['μMax'].append(resultado_fit.params["k"].value)
                tabela['A'].append(A)
                tabela["Fase lag"].append(inicio_intervalo)
                tabela["Growth Score"].append(GS)
            
            return tabela 


# -------------------------- Funçoes testes -------------------------

def cria_dataset_grafico(df_final, df_selecinados, modelo):
    """ Essa função seleciona no dataset principal dado(df_final) os poços de interesse do ususario, esses poços
        estão bem definidos no dataset(df_selecionados).

    Args:
        df_final (dataset): dataset com todas as placas e poços.
        df_selecinados (dataset): dataset contendo somente os poços que serão analizados.

    Returns:
        dataset: Um dataset contendo a coluna incial Tempo(horas) e o y_esperimental dos outros poços selecionados. 
    """
    
    df_grafico = pd.DataFrame()

    primeira_placa = next(iter(df_final.values()))  # Obtém o primeiro item do dicionário "dici"
    primeiro_poco = next(iter(primeira_placa.values()))  # Obtém o primeiro item do dicionário dentro da placa 


    # Acessando a primeira coluna do dataset (primeiro poço)
    primeira_coluna = primeiro_poco.iloc[:, 0]  # Seleciona a primeira coluna usando iloc

    df_grafico["Tempo(horas)"] = primeira_coluna

    if modelo == "Linear":
        for i in range(len(df_selecinados["Placa"])):

            placa = df_selecinados["Placa"][i]
            poços = df_selecinados["Poços"][i]

            y = df_final[placa][poços]["y_experimental"]


            log_coluna_y= np.log(y)

            df_grafico[f"{placa} - {poços}"] = log_coluna_y

        return df_grafico

    else:
        for i in range(len(df_selecinados["Placa"])):
            placa = df_selecinados["Placa"][i]
            poços = df_selecinados["Poços"][i]

            y = df_final[placa][poços]["y_experimental"]


            df_grafico[f"{placa} - {poços}"] = y
        
        return df_grafico

# --------------------- Função que gera gráficos --------------------


def plota_dataset_selecionado(df, titulo, legenda_x, legenda_y, legenda, fonte_selecionada, tamanho_legenda="12pt", tamanho_titulo="14pt"):
    """ 

    Args:
        df (_type_): _description_
        titulo (_type_): _description_
        legenda_x (_type_): _description_
        legenda_y (_type_): _description_
        legenda (_type_): _description_
        fonte_selecionada (_type_): _description_
        tamanho_legenda (str, optional): _description_. Defaults to "12pt".
        tamanho_titulo (str, optional): _description_. Defaults to "14pt".
    """


    # Configurações adicionais do usuário
    fonte_legenda = fonte_selecionada
    tamanho_titulo = f"{tamanho_titulo}pt"
    tamanho_legenda = f"{tamanho_legenda}pt"
    
    
    # Opções de cor e estilo para os eixos
    #cor_legenda_x = st.color_picker("Cor da legenda do eixo X", "#000000")
    #cor_legenda_y = st.color_picker("Cor da legenda do eixo Y", "#000000")
    #negrito_legenda_x = st.checkbox("Negrito no eixo X")
    #negrito_legenda_y = st.checkbox("Negrito no eixo Y")
    #negrito_titulo = st.checkbox("Negrito no título")
    

    p = figure(
        title=titulo,
        x_axis_label=legenda_x,
        y_axis_label=legenda_y,
        width=700,
        height=400,
        background_fill_color="white",
        border_fill_color="white",
        tools="box_zoom,reset,save, point_draw"
    )
    

    # Configuração do título
    p.title.text_font = fonte_legenda
    p.title.text_font_size = tamanho_titulo
    p.title.align = "center"
    p.title.text_color = "black"
    #p.title.text_font_style = "bold" if negrito_titulo else "normal"
    
    # Configuração dos eixos com as cores e estilos selecionados
    p.xaxis.axis_label_text_font = fonte_legenda
    p.yaxis.axis_label_text_font = fonte_legenda
    p.xaxis.axis_label_text_font_size = tamanho_legenda
    p.yaxis.axis_label_text_font_size = tamanho_legenda
    p.xaxis.axis_label_text_color = "#000000"
    p.yaxis.axis_label_text_color = "#000000"
    p.xaxis.axis_label_text_font_style = "bold" 
    p.yaxis.axis_label_text_font_style = "bold" 
    
    # Dados do eixo X
    eixo_x = df.iloc[:, 0]
    
    # Dados e legendas das séries do eixo Y
    colors = Dark2[8]
    legend_items = []
    for i in range(1, df.shape[1]):
        linha = p.line(
            eixo_x,
            df.iloc[:, i],
            line_width=2.5, 
            line_alpha=0.9, 
            color=colors[i % len(colors)]
        )
        legend_item = LegendItem(label=legenda[i - 1], renderers=[linha])
        legend_items.append(legend_item)


    legend = Legend(items=legend_items)

    p.add_layout(legend)
    p.legend.location = "bottom_right"
    
    # Exibindo o gráfico no Streamlit
    st.bokeh_chart(p)



