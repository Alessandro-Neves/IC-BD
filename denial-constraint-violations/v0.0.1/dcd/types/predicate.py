from enum import Enum
from dataclasses import dataclass

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
  