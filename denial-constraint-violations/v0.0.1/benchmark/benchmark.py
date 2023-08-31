import time
import pandas

from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector


dc_detector = DCDetector()

root_path = './testdatas'
ext = 'csv'
datasets = ['spotify_1k', 'spotify_5k', 'spotify_10k', 'spotify_20k', 'spotify_30k', 'spotify_40k']

results = [[], []]

for dataset in datasets:
  
  dc_reader = DCReader('./testdatas/spotify_170k_dc.txt')

  ss1 = Session(f'{root_path}/{dataset}.{ext}', dc_reader, dc_detector)
  ss2 = Session(f'{root_path}/{dataset}.{ext}', dc_reader, dc_detector)

  spotify_sessions = [ ss1, ss2 ]

  print(f"\nFor {dataset}:")
  for i, session in enumerate(spotify_sessions):
    init_time = time.time()
    session.detect_violations()
    end_time = time.time()
    
    t = end_time - init_time
    results[i].append(t)

print(results)


dataframe = pandas.DataFrame(results, columns=datasets)
nome_arquivo_saida = 'benchmark/results.csv'
dataframe.to_csv(nome_arquivo_saida, index=False)
