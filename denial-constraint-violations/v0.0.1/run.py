from dcd.core.dc_reader import DCReader
from dcd.types.predicate import Predicate
  
dc_reader = DCReader('dcs.txt')

print(dc_reader.get_str_dcs()[0])


