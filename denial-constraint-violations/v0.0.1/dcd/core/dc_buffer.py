from dcd.interfaces.dc_buffer import IDCBuffer
from typing import List

class DCBuffer(IDCBuffer):
  _dcs: List[List[str]]
  
  def __init__(self, constraints_file_path) -> None:
    
    with open(constraints_file_path, 'r') as file:
      lines = file.readlines()

    self._dcs = []
    for line in lines:
      line = line.strip()
      constraints = line.split(',')
      self._dcs.append(constraints)
  
  def get_all(self) -> List[List[str]]:
    return self._dcs