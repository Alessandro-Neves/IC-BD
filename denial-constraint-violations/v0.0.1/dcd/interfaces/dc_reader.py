from abc import ABC, abstractmethod
from dcd.types.predicate import Constraint

class IDCReader(ABC):
  @abstractmethod
  def __init__(self, constraints_file_path) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_str_dcs(self) -> list[list[Constraint]]:
    raise NotImplementedError
