from abc import ABC, abstractmethod
from typing import List

from dcd.types.predicate import Predicate

class IDC(ABC):  
  @abstractmethod
  def get_predicates(self) -> List[Predicate]:
    raise NotImplementedError