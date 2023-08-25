from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector

dc_reader = DCReader('dcs.txt')
dc_detector = DCDetector()
dc = DC(dc_reader)

session = Session('data.csv', dc, dc_detector)

session.detect_violations()

violations = session.get_violations()
clean_data = session.get_clean_cells()
noisy_data = session.get_noisy_cells()

# print(violations, end='\n\n')
# print(clean_data, end='\n\n')
# print(noisy_data, end='\n\n')

print(session.data,  end='\n\n')

for v in violations:
  print(v)



