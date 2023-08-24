from pandas import DataFrame, read_csv

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector

class Session():
  data: DataFrame
  noisy_cells: DataFrame | None
  clean_cells: DataFrame | None
  
  dc: IDC
  dc_detector: IDCDetector
  
  def __init__(self, data_address: str, dc: IDC, dc_detector: IDCDetector) -> None:
    self.data = read_csv(data_address)
    self.noisy_cells = None
    self.clean_cells = None
    
    self.dc = dc
    self.dc_detector = dc_detector
    
  def _detect_violations(self) -> None:
    self.noisy_cells = self.dc_detector.find_violations(self.dc)
    self.clean_cells = self.data[~self.data.apply(tuple, 1).isin(self.noisy_cells.apply(tuple, 1))] # type: ignore
  
  def find_violations(self) -> None:
    self._detect_violations()
  
  def get_clean_cells(self) -> DataFrame:
    if self.clean_cells is None:
      self._detect_violations()
      
    return self.clean_cells # type: ignore
  
  def get_noisy_cells(self) -> DataFrame:
    if self.noisy_cells is None:
      self._detect_violations()

    return self.noisy_cells # type: ignore