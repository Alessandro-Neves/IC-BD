from dataclasses import dataclass

from dcd.types.predicate import PredicateComponent
from dcd.types.predicate import PREDICATE_OPERATOR
from dcd.interfaces.predicate import IPredicate

@dataclass
class Predicate(IPredicate): 
  _constraint: str

  def get_operator(self) -> PREDICATE_OPERATOR:
    return self._constraint
  
  def get_left_side(self) -> PredicateComponent:
    return PredicateComponent(self._constraint, False)
  
  def get_right_side(self) -> PredicateComponent:
    return PredicateComponent(self._constraint, True)