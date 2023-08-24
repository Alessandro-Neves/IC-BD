from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector

dc_reader = DCReader('dcs.txt')
dc_detector = DCDetector()
dc = DC(dc_reader)

session = Session('data.csv', dc, dc_detector)

session.find_violations()

clean_data = session.get_clean_cells()
noisy_data = session.get_noisy_cells()

print(clean_data)
print(noisy_data)




