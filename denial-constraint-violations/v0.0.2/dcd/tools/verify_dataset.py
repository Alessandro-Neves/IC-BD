from pandas import read_csv, DataFrame

from dcd.interfaces.dc_reader import IDCReader
from dcd.interfaces.dc_detector import IDCDetector
from dcd.duck.dc_detector_verifier import DCDetectorVerifier

class DatasetOps():
  
  @staticmethod
  def count_violations(df: DataFrame, dc_reader: IDCReader) -> int:
    dc_detector = DCDetectorVerifier()
    
    dfc = df.copy()
    dfc.insert(0, '_id_', dfc.index)
    
    return dc_detector.find_violations(dfc, dc_reader.pop_dc())
  
  @staticmethod
  def is_clean_dataset(df: DataFrame, dc_reader: IDCReader, dc_detector: IDCDetector) -> bool:
    dfc = df.copy()
    
    dfc.insert(0, '_id_', dfc.index)
    
    dcs = dc_reader.get_dcs()

    return not any(bool(dc_detector.find_violations(dfc, dc)) for dc in dcs)
  
  @staticmethod
  def clean_dataset(df: DataFrame, dc_reader: IDCReader, dc_detector: IDCDetector) -> DataFrame:
    df.insert(0, '_id_', df.index)
    
    dcs = dc_reader.get_dcs()
    
    dropped_indexes = []
    
    for dc in dcs:
      violations = dc_detector.find_violations(df, dc)
      
      for violation in violations:
        if violation[0] not in dropped_indexes:
          df.drop(violation[0], inplace=True)
          dropped_indexes.append(violation[0])
        
        if violation[1] not in dropped_indexes:
          df.drop(violation[1], inplace=True)
          dropped_indexes.append(violation[1])
          
    return df.drop('_id_', axis=1)