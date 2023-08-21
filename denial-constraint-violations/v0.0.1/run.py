from dcd.interfaces.predicate import IPredicate
from dcd.types.predicate import PREDICATE_OPERATOR, PredicateComponent
from dcd.core.dc_buffer import DCBuffer
from dataclasses import dataclass


@dataclass
class Predicate(IPredicate): 
  _constraint: str

  def get_operator(self) -> PREDICATE_OPERATOR:
    return self._constraint
  
  def get_left_side(self) -> PredicateComponent:
    return PredicateComponent(self._constraint, False)
  
  def get_right_side(self) -> PredicateComponent:
    return PredicateComponent(self._constraint, True)
  
predicate = Predicate('t1.name > t2.name')

dc_buffer = DCBuffer('data.csv')

print(dc_buffer.get_all())
