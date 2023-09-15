import time

from dcd.core.dc import DC 
from dcd.core.session import Session 
from dcd.core.dc_reader import DCReader
from dcd.core.dc_detector import DCDetector
from dcd.duck.dc_detector import DCDetector as DuckDCDetector
from dcd.polars.dc_detector import DCDetector as PolarsDCDetector

# exit(0)
NOISY = True
ALIAS = '40k'

DC_FILE = 'testdatas/employees-dc.txt'
DATASET_FILE = f'testdatas/employees-{ALIAS}-noisy.csv' if NOISY else f'testdatas/employees-{ALIAS}.csv'

print("Pandas:")
dc_detector = DCDetector()

dc_reader = DCReader(DC_FILE)
session = Session(DATASET_FILE, dc_reader, dc_detector)

cur_time = time.monotonic()
session.detect_violations()
end_time = time.monotonic()

violations = session.get_violations()

print(len(violations))
print(end_time - cur_time)
print(violations)
print()


print("DuckDB:")
duck_dc_detector = DuckDCDetector()

dc_reader = DCReader(DC_FILE)
session = Session(DATASET_FILE, dc_reader, duck_dc_detector)

cur_time = time.monotonic()
session.detect_violations()
end_time = time.monotonic()

violations = session.get_violations()

print(len(violations))
print(end_time - cur_time)
# print(violations)
print()


# clean_data = session.get_clean_cells()
# noisy_data = session.get_noisy_cells()

# # OUTPUT

# print(session.data,  end='\n\n')



# print('clean cells:')
# print(clean_data, end='\n\n')
# print('noisy cells:')
# print(noisy_data, end='\n\n')

print("Polars:")
polars_dc_detector = PolarsDCDetector()

dc_reader = DCReader(DC_FILE)
session = Session(DATASET_FILE, dc_reader, polars_dc_detector)

cur_time = time.monotonic()
session.detect_violations()
end_time = time.monotonic()

violations = session.get_violations()

print(len(violations))
print(end_time - cur_time)
# print(violations)
print()


# for v in violations:
#   print(v)
# print('\n')