import pandas

from dcd.core.dc_reader import DCReader
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
# from dcd.duck.dc_detector_verifier import DCDetectorVerifier as DuckDCDetector

from dcd.tools.dataset_operations import DatasetOps

ROOT_PATH = 'testdatas'

configs = [
  # {'dataset': 'employees_40000.csv', 'dcs': ['employees_dc.txt']},
  # {'dataset': 'tax_1000000.csv', 'dcs': ['tax_dc1.txt', 'tax_dc2.txt']},
  # {'dataset': 'lineitem_1000000.csv', 'dcs': ['lineitem_dc1.txt', 'lineitem_dc2.txt', 'lineitem_dc3.txt']},
  # {'dataset': 'lineorder_1000000.csv', 'dcs': ['lineorder_dc1.txt']},
  {'dataset': 'flights_100000.csv', 'dcs': ['flights_dc2.txt']},
  
]

dc_detector = DuckDCDetector()

for config in configs:
  dataset_file = f'{ROOT_PATH}/original_datasets/' + config['dataset']
  output_file = f'{ROOT_PATH}/clean_datasets/' + config['dataset']
  
  df = pandas.read_csv(dataset_file)

  for dc_address in config['dcs']:
    dc_file_address = f'{ROOT_PATH}/dcs/{dc_address}'
    dc_reader = DCReader(dc_file_address)
    df = DatasetOps.clean_dataset(df, dc_reader, dc_detector)
    
    is_clean = DatasetOps.is_clean_dataset(df, dc_reader, dc_detector)
    print(f"{config['dataset']}:\t", "CLEAN" if is_clean else "NOISY", f"\t\t{dc_address}")
    
  df.to_csv(output_file, index=False) # type: ignore
  
    
    