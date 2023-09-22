import pandas as pd
import random

# Carrega o arquivo CSV
nome_arquivo_entrada = str(input("Input: "))
nome_arquivo_saida = str(input("Output: "))
n_linhas_aleatorias = int(input("Cut to: "))

# Carrega o arquivo CSV para um DataFrame
dataframe = pd.read_csv(nome_arquivo_entrada)

# Seleciona aleatoriamente n linhas do DataFrame
linhas_aleatorias = random.sample(range(len(dataframe)), n_linhas_aleatorias)
dataframe_aleatorio = dataframe.iloc[linhas_aleatorias]

# Salva as linhas aleatórias em um novo arquivo CSV
dataframe_aleatorio.to_csv(nome_arquivo_saida, index=False)