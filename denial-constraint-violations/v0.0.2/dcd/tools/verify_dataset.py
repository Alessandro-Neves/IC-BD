from pandas import read_csv

from dcd.interfaces.dc_reader import IDCReader
from dcd.interfaces.dc_detector import IDCDetector
class DatasetOps():
  
  @staticmethod
  def is_clean_dataset(csv_address: str, dc_reader: IDCReader, dc_detector: IDCDetector) -> bool:
    df = read_csv(csv_address)
    dcs = dc_reader.get_dcs()

    return not any(bool(dc_detector.find_violations(df, dc)) for dc in dcs)