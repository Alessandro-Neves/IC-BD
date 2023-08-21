from dcd.interfaces.predicate import IPredicate
from dcd.types.predicate import PREDICATE_OPERATOR, PredicateComponent

class Predicate(IPredicate): 
  def __init__(self, constraint: str) -> None:
    self.constraint: str = constraint
  
  def get_operator(self) -> PREDICATE_OPERATOR:
    return self.constraint
  
  def get_left_side(self) -> PredicateComponent:
    return PredicateComponent(self.constraint, False)
  
  def get_right_side(self) -> PredicateComponent:
    return PredicateComponent(self.constraint, True)
  
p = Predicate()

print(1)