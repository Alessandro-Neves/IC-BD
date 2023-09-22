from dcd.core.dc_reader import DCReader
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
# from dcd.duck.dc_detector_verifier import DCDetectorVerifier as DuckDCDetector

from dcd.tools.dataset_operations import DatasetOps

import pandas as pd

ROOT_PATH = 'testdatas'

configs = [
  {'dataset': 'employees_40000.csv', 'dcs': ['employees_dc.txt']},
  {'dataset': 'tax_1000000.csv', 'dcs': ['tax_dc1.txt', 'tax_dc2.txt', 'tax_dc4.txt']},
  # {'dataset': 'lineitem_1000000.csv', 'dcs': ['lineitem_dc1.txt', 'lineitem_dc2.txt', 'lineitem_dc3.txt']},
  # {'dataset': 'lineorder_1000000.csv', 'dcs': ['lineorder_dc1.txt']},
]

for config in configs:
  dataset_file = f'{ROOT_PATH}/clean_datasets/' + config['dataset']
  
  df = pd.read_csv(dataset_file)

  for dc_address in config['dcs']:
    dc_file_address = f'{ROOT_PATH}/dcs/{dc_address}'
    dc_reader = DCReader(dc_file_address)
    vio_qtd = DatasetOps.count_violations(df, dc_reader.pop_dc())
    
    print(f"{config['dataset']}:\t", "CLEAN" if not vio_qtd else "NOISY", f"\t\t{dc_address}")