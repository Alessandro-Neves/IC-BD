import pandas as pd

from dcd.tools.dataset_operations import DatasetOps
from dcd.core.dc_reader import DCReader
from dcd.types.predicate import PREDICATE_OPERATOR
import random

from config import DC_FILE, DATASET_FILE

WITH_EQUALITY_OPERATORS = [
  PREDICATE_OPERATOR.EQ,
  PREDICATE_OPERATOR.GTE,
  PREDICATE_OPERATOR.LTE
]

NOISY_PERCENTAGE = 10

dc = DCReader(DC_FILE).pop_dc()

df = pd.read_csv(DATASET_FILE)
dfc = df.copy()

num_tuples = df.shape[0]

desired_noisy_qtd = int(num_tuples * (NOISY_PERCENTAGE / 100))

NOISY_RANGE_ERROR = (desired_noisy_qtd * 0.05)

num_violations = 0

print("Try generate violations: ", desired_noisy_qtd)

iterations = 0

for it in range(100000):
  iterations = it
  if (num_violations > desired_noisy_qtd - NOISY_RANGE_ERROR):
    break
  
  idx1 = random.randint(0, num_tuples - 1)
  idx2 = random.randint(0, num_tuples - 1)
  
  dft = novo_df = df.copy().loc[[idx1, idx2]]
  
  vio_qtd = DatasetOps.count_violations(dft, dc)
  
  if vio_qtd == 0:
    predicates = dc.get_predicates()
    for predicate in predicates:
      col_name_A = predicate.left_side.col_name_or_value
      col_name_B = predicate.right_side.col_name_or_value
    
      # If 𝜌 ∈ {=, ≤, ≥}, change t[𝐴] -> t[𝐵]
      if predicate.operator in WITH_EQUALITY_OPERATORS:
        dfc.at[idx1, col_name_A] = dfc.at[idx2, col_name_B]
      # If 𝜌 ∈ {<, >, ≠}, change t[A] to another value from the active domain of the attribute such that 𝑃 is satisfied
      else: 
        if not predicate.operator == PREDICATE_OPERATOR.IQ:
          continue
          
        new_value = dfc.at[idx2, col_name_B] + 1 if predicate.operator == PREDICATE_OPERATOR.GT else -1
        dfc.at[idx1, col_name_A] = new_value
  
      vio_qtd_dfc = len(DatasetOps.tuples_on_violations(dfc, dc))
      
      print(vio_qtd_dfc)
      
      if vio_qtd_dfc > num_violations and vio_qtd_dfc < (desired_noisy_qtd + NOISY_RANGE_ERROR):
        df = dfc.copy()
        num_violations = vio_qtd_dfc
      else:
        dfc = df.copy()

print("Iterations: ", iterations)
print("Violations: ",DatasetOps.count_violations(df, dc))
print("Tuples on some violation: ", len(DatasetOps.tuples_on_violations(df, dc)))

df.to_csv(f'flights_noisy_{NOISY_PERCENTAGE}.csv', index=False) # type: ignore