from abc import ABC, abstractmethod
from dcd.types.predicate import Constraint

class IDCBuffer(ABC):
  @abstractmethod
  def __init__(self, constraints_file_path) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_all(self) -> list[list[Constraint]]:
    raise NotImplementedError
