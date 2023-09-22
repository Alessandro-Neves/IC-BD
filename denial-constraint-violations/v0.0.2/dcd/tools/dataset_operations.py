from pandas import read_csv, DataFrame
from typing import List

from dcd.interfaces.dc_reader import IDCReader
from dcd.interfaces.dc_detector import IDCDetector
from dcd.duck.dc_detector_verifier import DCDetectorVerifier
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from dcd.interfaces.dc import IDC

class DatasetOps():
  
  @staticmethod
  def count_violations(df: DataFrame, dc: IDC) -> int:
    dc_detector = DCDetectorVerifier()
    
    dfc = df.copy()
    dfc.insert(0, '_id_', dfc.index)
    
    return dc_detector.find_violations(dfc, dc)
  
  @staticmethod
  def tuples_on_violations(df: DataFrame, dc: IDC) -> List[int]:
    dc_detector = DuckDCDetector()

    dfc = df.copy()
    dfc.insert(0, '_id_', dfc.index)

    vio_pairs = dc_detector.find_violations(dfc, dc)
    
    ids = [id for tupla in vio_pairs for id in tupla]
    
    return list(set(ids))
  
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
      
      ids = [id for tupla in violations for id in tupla]
      
      ids_to_rm = list(set(ids))
      
      for i, id_index in enumerate(ids_to_rm):
        print(f"{i}/{len(ids_to_rm)}", id_index)
        df.drop(id_index, inplace=True)
        
        # if violation[0] not in dropped_indexes:
          
        #   dropped_indexes.append(violation[0])
        
        # if violation[1] not in dropped_indexes:
        #   df.drop(violation[1], inplace=True)
        #   dropped_indexes.append(violation[1])
          
    return df.drop('_id_', axis=1)