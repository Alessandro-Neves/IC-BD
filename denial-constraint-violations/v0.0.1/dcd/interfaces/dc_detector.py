from abc import ABC, abstractmethod
from pandas import DataFrame

from dcd.interfaces.dc import IDC

class IDCDetector(ABC):
  
  @abstractmethod
  def find_violations(self, df: DataFrame, dc: IDC) -> DataFrame:
    raise NotImplementedError