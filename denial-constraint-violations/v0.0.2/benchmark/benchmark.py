import time
import pandas

from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector

################ 1 DC, Many DcDetectors #########################

dc_detector = DCDetector()
duck_dc_detector = DuckDCDetector()
polars_dc_detector = PolarsDCDetector()

root_path = 'testdatas/dirty_datasets'
ext = 'csv'

datasets = ['employees-1k-noisy', 'employees-5k-noisy', 'employees-10k-noisy', 'employees-20k-noisy', 'employees-40k-noisy']

results = [[], [], []]

for dataset in datasets:
  
  dc_reader1 = DCReader('benchmark/dc.txt')
  dc_reader2 = DCReader('benchmark/dc.txt')
  dc_reader3 = DCReader('benchmark/dc.txt')

  ss1 = Session(f'{root_path}/{dataset}.{ext}', dc_reader1, dc_detector)
  ss2 = Session(f'{root_path}/{dataset}.{ext}', dc_reader2, polars_dc_detector)
  ss3 = Session(f'{root_path}/{dataset}.{ext}', dc_reader3, duck_dc_detector)
  # ss4 = Session(f'{root_path}/{dataset}.{ext}', dc_reader4, duck_dc_detector_distinct)

  spotify_sessions = [ ss1, ss2, ss3 ]

  print(f"\nFor {dataset}:")
  for i, session in enumerate(spotify_sessions):
    init_time = time.time()
    session.detect_violations()
    end_time = time.time()
    
    t = end_time - init_time
    results[i].append(t)

print(results)


dataframe = pandas.DataFrame(results, columns=datasets)
nome_arquivo_saida = 'benchmark/results_many_detectors.csv'
dataframe.to_csv(nome_arquivo_saida, index=False)

exit(0)

################# Many DC, 1 DcDetector ###############################


dc_detector = DCDetector()

root_path = 'testdatas'
ext = 'csv'
datasets = ['spotify_1k', 'spotify_5k', 'spotify_10k', 'spotify_20k', 'spotify_30k', 'spotify_40k', 'spotify_80k', 'spotify_120k', 'spotify_170k_id']
# datasets = ['spotify_1k', 'spotify_5k', 'spotify_10k']

results = [[], [], []]

for dataset in datasets:
  
  dc_reader = DCReader('benchmark/dcs.txt')

  ss1 = Session(f'{root_path}/{dataset}.{ext}', dc_reader, dc_detector)
  ss2 = Session(f'{root_path}/{dataset}.{ext}', dc_reader, dc_detector)
  ss3 = Session(f'{root_path}/{dataset}.{ext}', dc_reader, dc_detector)

  spotify_sessions = [ ss1, ss2, ss3 ]

  print(f"\nFor {dataset}:")
  for i, session in enumerate(spotify_sessions):
    init_time = time.time()
    session.detect_violations()
    end_time = time.time()
    
    t = end_time - init_time
    results[i].append(t)

print(results)


dataframe = pandas.DataFrame(results, columns=datasets)
nome_arquivo_saida = 'benchmark/results_one_detector.csv'
dataframe.to_csv(nome_arquivo_saida, index=False)