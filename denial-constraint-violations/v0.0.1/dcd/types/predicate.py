from enum import Enum
from typing import Any
from dataclasses import dataclass

class PREDICATE_OPERATOR(Enum):
  """Enum OPERATOR"""
  EQ = '='
  IQ = '<>'
  LT = '<'
  LTE = '<='
  GT = '>'
  GTE = '>='
  
def get_PREDICATE_OPERATOR_by_key(key):
  enums_by_keys = {i.value: i for i in PREDICATE_OPERATOR}
  return enums_by_keys.get(key)
  
@dataclass
class PredicateComponent:
  col_name_or_value: Any
  is_scalar_value: bool
  
Constraint = str

@dataclass
class Predicate: 
  left_side: PredicateComponent
  operator: PREDICATE_OPERATOR
  right_side: PredicateComponent
  is_relational: bool
  has_diff_target: bool