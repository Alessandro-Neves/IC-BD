from abc import ABC, abstractmethod
from dcd.types.predicate import PREDICATE_OPERATOR, PredicateComponent

class IPredicate(ABC):
  
  @abstractmethod
  def get_operator(self) -> PREDICATE_OPERATOR:
    raise NotImplementedError
  
  @abstractmethod
  def get_left_side(self) -> PredicateComponent:
    raise NotImplementedError
  
  @abstractmethod
  def get_right_side(seld) -> PredicateComponent:
    raise NotADirectoryError

