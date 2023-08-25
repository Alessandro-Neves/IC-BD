from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector

dc_reader = DCReader('dcs.txt')
dc_detector = DCDetector()
session = Session('mid.csv', dc_reader, dc_detector)

session.detect_violations()

violations = session.get_violations()
clean_data = session.get_clean_cells()
noisy_data = session.get_noisy_cells()

# OUTPUT

print(session.data,  end='\n\n')

for v in violations:
  print(v)
print('\n')



print('clean cells:')
print(clean_data, end='\n\n')
print('noisy cells:')
print(noisy_data, end='\n\n')