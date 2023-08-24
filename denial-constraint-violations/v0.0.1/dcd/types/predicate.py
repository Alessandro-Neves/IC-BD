from enum import Enum
from dataclasses import dataclass

from dcd.types.predicate import PredicateComponent
from dcd.types.predicate import PREDICATE_OPERATOR

class PREDICATE_OPERATOR(Enum):
  """Enum OPERATOR"""
  EQ = '='
  IQ = '<>'
  LT = '<'
  LTE = '<='
  GT = '>'
  GTE = '>='
  
@dataclass
class PredicateComponent:
  col_name_or_value: any
  is_scalar_value: bool
  
Constraint = str

@dataclass
class Predicate: 
  left_side: PredicateComponent
  operator: PREDICATE_OPERATOR
  right_side: PredicateComponent