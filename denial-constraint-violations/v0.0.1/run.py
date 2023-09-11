import time

from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector

# exit(0)

dc_detector = DCDetector()

dc_reader = DCReader('testdatas/spotify_170k_dc.txt')

session = Session('testdatas/spotify_10k.csv', dc_reader, dc_detector)

cur_time = time.monotonic()
session.detect_violations()
end_time = time.monotonic()

print(end_time - cur_time)


violations = session.get_violations()
print(len(violations), end='\n\n')

for v in violations:
  print(v)
print('\n')

duck_dc_detector = DuckDCDetector()

dc_reader = DCReader('testdatas/spotify_170k_dc.txt')

session = Session('testdatas/spotify_10k.csv', dc_reader, duck_dc_detector)

cur_time = time.monotonic()
session.detect_violations()
end_time = time.monotonic()

print(end_time - cur_time)


violations = session.get_violations()
print(len(violations), end='\n\n')

for v in violations:
  print(v)
print('\n')

# for v in violations:
#   print(v)
# print('\n')


# clean_data = session.get_clean_cells()
# noisy_data = session.get_noisy_cells()

# # OUTPUT

# print(session.data,  end='\n\n')



# print('clean cells:')
# print(clean_data, end='\n\n')
# print('noisy cells:')
# print(noisy_data, end='\n\n')