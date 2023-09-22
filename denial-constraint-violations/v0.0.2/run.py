import time
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector

from config import DC_FILE, DATASET_FILE

detectors = [
  # DCDetector(),
  # PolarsDCDetector(),
  DuckDCDetector(),
]

names = [
  # "Pandas", 
  # "Polars", 
  "Duck JOIN"
]

for i, detector in enumerate(detectors):
  print(f"{names[i]}: ")
  dc_detector = detector
  dc_reader = DCReader(DC_FILE)
  session = Session(DATASET_FILE, dc_reader, dc_detector)
  
  cur_time = time.monotonic()
  session.detect_violations()
  end_time = time.monotonic()
  
  violations = session.get_violations()
  
  print(len(violations))
  print(end_time - cur_time)
  print(violations)
  print()