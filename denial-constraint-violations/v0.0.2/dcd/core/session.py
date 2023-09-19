import copy
from pandas import DataFrame, read_csv

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_reader import IDCReader
from dcd.interfaces.dc_detector import IDCDetector
from dcd.types.common import PairIdList

class Session():
  data: DataFrame
  violations: PairIdList
  
  dc: IDC
  dc_detector: IDCDetector
  
  def __init__(self, data_address: str, dc_reader: IDCReader, dc_detector: IDCDetector) -> None:
    self.data = read_csv(data_address)
    self.data.insert(0, '_id_', self.data.index)
    
    self.dc = dc_reader.pop_dc()
    self.dc_detector = dc_detector
    
  def detect_violations(self) -> None:
    self.violations = self.dc_detector.find_violations(copy.deepcopy(self.data), self.dc)
  
  def get_violations(self) -> PairIdList:
    return self.violations
  
  def get_clean_cells(self) -> DataFrame:
    return self.data[~self.data['_id_'].isin([it[0] for it in self.violations])]
  
  def get_noisy_cells(self) -> DataFrame:
    return self.data[self.data['_id_'].isin([it[0] for it in self.violations])]