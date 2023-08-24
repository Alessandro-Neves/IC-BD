from dcd.types.predicate import Constraint, PredicateComponent

class DCParser:
  def __init__(self, dc_constraints: list[Constraint]) -> None:
    raise NotImplementedError
  
  def get_predicates(self) -> list[PredicateComponent]:
    raise NotImplementedError
