import time, pandas
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.duck.dc_detector import DCDetector as DuckDCDetector

from dcd.tools.dataset_operations import DatasetOps

from config import DC_FILE, DATASET_FILE

dc_detector = DuckDCDetector()
dc = DCReader(DC_FILE).pop_dc()

df = pandas.read_csv(DATASET_FILE)

vio_qtd = DatasetOps.count_violations(df, dc)
tuples_on_violations = DatasetOps.tuples_on_violations(df, dc)

print("Violations: ", vio_qtd)
print("Tuples on violations: ", len(tuples_on_violations))