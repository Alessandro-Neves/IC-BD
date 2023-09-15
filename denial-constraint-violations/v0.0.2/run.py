import time
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from dcd.duck.dc_detector_sql import DCDetector as DuckDistinticDCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector

# exit(0)
NOISY = True
ALIAS = '10k'

DC_FILE = 'testdatas/employees-dc.txt'
DATASET_FILE = f'testdatas/employees-{ALIAS}-noisy.csv' if NOISY else f'testdatas/employees-{ALIAS}.csv'


detectors = [
  DCDetector(),
  PolarsDCDetector(),
  DuckDCDetector(),
  DuckDistinticDCDetector()
]

names = ["Pandas", "Polars", "Duck JOIN", "Duck DISTINCT"]

for i, detector in enumerate(detectors):
  print(f"{names[i]}: ")
  dc_detector = detector
  dc_reader = DCReader(DC_FILE)
  session = Session(DATASET_FILE, dc_reader, dc_detector)
  
  cur_time = time.monotonic()
  session.detect_violations()
  end_time = time.monotonic()
  
  violations = session.get_violations()
  
  # print(len(violations))
  print(end_time - cur_time)
  # print(violations)
  print()