import time
import pandas as pd
import matplotlib.pyplot as plt


from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector
from dcd.tools.dataset_operations import DatasetOps
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from dcd.duck.dc_detector_distinct import DCDetector as DuckDistinctDCDetector
from noisy_generator import gen_noisy_df

ROOT_FOLDER = 'benchmark/testdatas/tax/dc1'
DC_FILE = ROOT_FOLDER + '/dc.txt'
OUTPUT_FILE = ROOT_FOLDER + '/results.txt'

noises_percentages = [
  0.01,
  0.05,
  0.1,
  0.5,
  1,
]

test_average = 3

################ 1 DC, Many DcDetectors #########################
dc_detectors = [
  DuckDCDetector(),
  DuckDCDetector(),
  DuckDCDetector(),
]

dc = DCReader(DC_FILE).pop_dc()

results = [[] for _ in dc_detectors]

for i, dc_detector in enumerate(dc_detectors):
  for noisy_percentage in noises_percentages:
    
    df = pd.read_csv(f"{ROOT_FOLDER}/{noisy_percentage}.csv")

    # noisy_df = gen_noisy_df(dc, df, noisy_percentage)
    
    noisy_with_id = df.copy()
    noisy_with_id.insert(0, '_id_', noisy_with_id.index)
    
    total_time = 0
    for _ in range(test_average):
      init_time = time.time()
      dc_detector.find_violations(noisy_with_id, dc)
      end_time = time.time()
      
      total_time = end_time - init_time
      
    t = total_time / test_average
    
    results[i].append(t)
  
results_df = pd.DataFrame(results, columns=noises_percentages)
results_df.to_csv(OUTPUT_FILE, index=False)



collumns = results_df.columns.tolist()

dc1_times = results_df.iloc[0].values.astype(float)
dc2_times = results_df.iloc[1].values.astype(float)
dc3_times = results_df.iloc[2].values.astype(float)
# dc4_times = results_df.iloc[3].values.astype(float)

x_indexes = [str(v) for v in collumns]

plt.plot(x_indexes, dc1_times, marker='o', label='DuckDB')
plt.plot(x_indexes, dc2_times, marker='o', label='Polars')
plt.plot(x_indexes, dc3_times, marker='o', label='Pandas')
# plt.plot(x_indexes, dc3_times, marker='o', label='DuckDB')


plt.title('1 DC, Many DCDetectors')
plt.xlabel('Tuples involved in violations (%)')
plt.ylabel('Time exec (s)')
plt.grid(True)
plt.legend()  # Mostra a legenda

# Salvar o gráfico como uma imagem na pasta
plt.savefig(ROOT_FOLDER + '/results.png')

# Limpar o buffer de plots (se você deseja criar mais gráficos)
plt.clf()