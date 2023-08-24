from dcd.interfaces.dc_reader import IDCReader
from typing import List

class DCReader(IDCReader):
  _dcs: List[List[str]]
  
  def __init__(self, constraints_file_path) -> None:
    
    with open(constraints_file_path, 'r') as file:
      lines = file.readlines()

    self._dcs = []
    for line in lines:
      line = line.strip()
      constraints = line.split(',')
      self._dcs.append(constraints)
  
  def get_str_dcs(self) -> List[List[str]]:
    return self._dcs