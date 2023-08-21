from abc import ABC, abstractmethod
from .dc_buffer import IDCBuffer
from .predicate import IPredicate

class IDCParser(ABC):
  @abstractmethod
  def __init__(self, dc_buffer: IDCBuffer) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_predicates(self) -> list[IDCBuffer]:
    raise NotImplementedError
