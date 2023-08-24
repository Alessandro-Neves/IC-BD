from abc import ABC, abstractmethod
from typing import List
from dcd.types.predicate import Constraint

class IDCReader(ABC):
  @abstractmethod
  def __init__(self, constraints_file_path) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_str_dcs(self) -> List[List[Constraint]]:
    raise NotImplementedError
  
  @abstractmethod
  def pop_dc_str(self) -> List[str]:
    raise NotImplementedError