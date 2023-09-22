import pandas as pd

nome_arquivo_entrada = 'testdatas/spotify_170k.csv'
nome_arquivo_saida = 'testdatas/spotify_170k_id.csv'

dataframe = pd.read_csv(nome_arquivo_entrada)

if 'id' in dataframe.columns:
  dataframe.drop(columns=['id'], inplace=True)

dataframe['id'] = dataframe.index

colunas = dataframe.columns.tolist()
colunas = ['id'] + [coluna for coluna in colunas if coluna != 'id']
dataframe = dataframe[colunas]

dataframe.to_csv(nome_arquivo_saida, index=False)