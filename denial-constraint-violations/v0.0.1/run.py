from dcd.core.dc_reader import DCReader
from dcd.core.dc import DC
  
dc_reader = DCReader('dcs.txt')

dc = DC(dc_reader)

print(dc.get_predicates()[0])

print(dc_reader.get_str_dcs()[0])



