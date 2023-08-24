from abc import ABC, abstractmethod
from typing import List

from dcd.interfaces.dc_reader import IDCReader
from dcd.types.predicate import Predicate

class IDC(ABC):
  @abstractmethod
  def __init__(self, dc_reader: IDCReader) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_predicates(self) -> List[Predicate]:
    raise NotImplementedError