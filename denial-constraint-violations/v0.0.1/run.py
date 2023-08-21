from dcd.core.dc_buffer import DCBuffer
from dcd.core.predicate import Predicate
  
predicate = Predicate('t1.name > t2.name')

dc_buffer = DCBuffer('data.csv')

print(predicate.get_left_side())
print(dc_buffer.get_all())
