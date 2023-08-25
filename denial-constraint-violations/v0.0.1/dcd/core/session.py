import copy
from pandas import DataFrame, read_csv

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector
from dcd.types.common import AdjacencyList

class Session():
  data: DataFrame
  violations: AdjacencyList
  
  dc: IDC
  dc_detector: IDCDetector
  
  def __init__(self, data_address: str, dc: IDC, dc_detector: IDCDetector) -> None:
    self.data = read_csv(data_address)
    
    self.dc = dc
    self.dc_detector = dc_detector
    
  def detect_violations(self) -> None:
    self.violations = self.dc_detector.find_violations(copy.deepcopy(self.data), self.dc)
  
  def get_violations(self) -> AdjacencyList:
    return self.violations
  
  def get_clean_cells(self) -> DataFrame:
    return self.data[~self.data['id'].isin([it[0] for it in self.violations])]
  
  def get_noisy_cells(self) -> DataFrame:
    return self.data[self.data['id'].isin([it[0] for it in self.violations])]