import pandas as pd
import numpy as np


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

#______________________________________________________________________________________________________________________________________________


def df_triplicatas(dataset):
    """
    Processa um dataset de experimentos com triplicatas, calculando a média das triplicatas e transformando a primeira 
    coluna de tempo de minutos para horas. Retorna um novo DataFrame com as médias e o tempo convertido.

    O dataset é esperado no seguinte formato:
    - A primeira coluna corresponde ao tempo (em minutos).
    - As colunas subsequentes são divididas em grupos de três (triplicatas) para cada poço experimental.

    O novo DataFrame terá a primeira coluna transformada de minutos para horas, e para cada triplicata, será 
    criada uma nova coluna com a média dos valores das três colunas originais.

    Args:
        dataset: DataFrame do pandas contendo os dados experimentais. 
    
    return: 
        DataFrame com a primeira coluna sendo o tempo em horas, e as colunas das triplicatas substituídas pelas médias.
    """

    dataset_sem_triplicatas = pd.DataFrame(dataset.iloc[:,0]) # Reservando a primeira coluna do dataset, correspondente ao tempo. 

    dataset_sem_triplicatas.columns = ['Tempo(horas)'] + list(dataset_sem_triplicatas.columns[1:])  # Substitua 'Novo_Nome' pelo nome desejado

    # Divide os valores da primeira coluna por 60
    dataset_sem_triplicatas["Tempo(horas)"] = dataset_sem_triplicatas["Tempo(horas)"] / 60 #transformando o tempo de minutos para hora


    colunas = int((len(dataset.columns) - 1) / 3)

    letras_colunas = ["A","B","C","D","E","F","G","H",]

    letra = 0

    passo = 1

    for i in range(1, colunas + 1):
        
        colunas_para_media = dataset.iloc[:, (i*3 -2) : (i*3+1)]  # Substitua 0:3 pelos índices das colunas desejadas

        # Calcula a média das três colunas para cada linha
        media_colunas = colunas_para_media.mean(axis=1)


        # Cria um novo DataFrame e adiciona a coluna com as médias
        dataset_sem_triplicatas[f'Poço-{letras_colunas[letra]}({(passo*3-2)}-{(passo*3)})'] = media_colunas

        if (i % 4) == 0:
            letra += 1
        
        if passo == 4:
            passo = 1
        else:
            passo += 1

    return dataset_sem_triplicatas


#____________________________________________________________________________________________________________________


def construir_dici_poços(dataset):
    """
    Constrói um dicionário onde cada chave é o nome de uma coluna (exceto a primeira) do dataset,
    e o valor é um subconjunto do dataset contendo a primeira coluna e a coluna correspondente.

    Args:
        dataset: DataFrame do pandas com os dados.

    return: 
        Dicionário onde as chaves são os nomes das colunas (exceto a primeira)
        e os valores são DataFrames contendo a primeira coluna e a respectiva coluna.
    """

    primeira_coluna = dataset.columns[0]

    # Criando o dicionário com as colunas (exceto a primeira) e os respectivos datasets
    return {col: dataset[[primeira_coluna, col]] for col in dataset.columns[1:]}

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

    for dados in dados_brutos: 
        df_reduzido = df_triplicatas(dados)
        lista_df_destriplicados.append(df_reduzido)

    lista_dici_poços = []

    for df in lista_df_destriplicados:
        dici_poços = construir_dici_poços(df)
        lista_dici_poços.append(dici_poços)
    

    dici_placas = construir_dici_placas(lista_dici_poços)

    return dici_placas




