from pandas import DataFrame

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector

class DCDetector(IDCDetector):
  
  def find_violations(self, df: DataFrame, dc: IDC) -> DataFrame:
    return df.head(3)