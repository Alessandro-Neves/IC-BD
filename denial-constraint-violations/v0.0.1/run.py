from dcd.core.dc_reader import DCReader
from dcd.types.predicate import Predicate
  
# predicate = Predicate('t1.name > t2.name')
dc_reader = DCReader('dcs.txt')

# print(predicate.get_left_side())
print(dc_reader.get_str_dcs()[0])

