import time, pandas
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.duck.dc_detector import DCDetector as DuckDCDetector

from dcd.tools.verify_dataset import DatasetOps

from config import DC_FILE, DATASET_FILE

dc_detector = DuckDCDetector()
dc_reader = DCReader(DC_FILE)

df = pandas.read_csv(DATASET_FILE)

vio_qtd = DatasetOps.count_violations(df, dc_reader)

print("Violations: ", vio_qtd)