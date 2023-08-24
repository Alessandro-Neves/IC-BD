from dataclasses import dataclass
from typing import List

from dcd.types.predicate import Predicate

@dataclass
class DC:
  predicates: List[Predicate]