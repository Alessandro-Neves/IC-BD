from abc import ABC, abstractmethod
from ..types.predicate import PREDICATE_OPERATOR, PredicateComponent

__all__ = ["IConstraint"]

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

