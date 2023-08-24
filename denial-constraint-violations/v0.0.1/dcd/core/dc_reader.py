from dcd.types.predicate import Constraint
from dcd.interfaces.dc_reader import IDCReader
from typing import List

class DCReader(IDCReader):
  _dc: List[List[str]]
  
  def __init__(self, constraints_file_path) -> None:
    
    with open(constraints_file_path, 'r') as file:
      lines = file.readlines()

    self._dc = []
    for line in lines:
      line = line.strip()
      constraints = line.split(',')
      self._dc.append(constraints)
      
  def get_str_dcs(self) -> List[List[Constraint]]:
    return self._dc
  
  def pop_dc_str(self) -> List[str]:
    return self._dc.pop()