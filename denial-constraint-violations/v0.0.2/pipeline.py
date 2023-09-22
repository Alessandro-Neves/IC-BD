import time
import pandas as pd
import matplotlib.pyplot as plt


from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from pipeline_config import USE_CONFIG

config = USE_CONFIG

ROOT_FOLDER = config['root_path']
DC_FILE = ROOT_FOLDER + '/dc.txt'
OUTPUT_FILE = ROOT_FOLDER + '/results.txt'

noises_percentages = config['noises_percentages']
times = config['times']

dc_detectors = [
  DuckDCDetector(),
  DuckDCDetector(),
  DuckDCDetector()
]

dc = DCReader(DC_FILE).pop_dc()
results = [[] for _ in dc_detectors]

max_iterations = len(dc_detectors) * times * len(noises_percentages)
iterations = 0

for i, dc_detector in enumerate(dc_detectors):
  for noisy_percentage in noises_percentages:
    
    df = pd.read_csv(f"{ROOT_FOLDER}/{noisy_percentage}.csv")

    # noisy_df = gen_noisy_df(dc, df, noisy_percentage)
    
    noisy_with_id = df.copy()
    noisy_with_id.insert(0, '_id_', noisy_with_id.index)
    
    total_time = 0
    for _ in range(times):
      init_time = time.time()
      dc_detector.find_violations(noisy_with_id, dc)
      end_time = time.time()
      
      total_time = end_time - init_time
      
      iterations += 1
      print(f"{iterations}/{max_iterations}")
      
    t = total_time / times
    
    results[i].append(t)
  
results_df = pd.DataFrame(results, columns=noises_percentages)
results_df.to_csv(OUTPUT_FILE, index=False)

collumns = results_df.columns.tolist()

## PLOT

dc_detectors_names = [
  'DuckDB',
  'Polars',
  'Pandas',
]

x_indexes = [str(v) for v in collumns]

for i, _ in enumerate(dc_detectors):
  plt.plot(
    x_indexes, 
    results_df.iloc[i].values.astype(float),
    marker='o', 
    label=dc_detectors_names[i]
  )

plt.title(config['title'] + f" {times} times")
plt.xlabel('Tuples involved in violations (%)')
plt.ylabel('Time exec (s)')
plt.grid(True)
plt.legend()

plt.savefig(ROOT_FOLDER + '/results.png')
plt.clf()