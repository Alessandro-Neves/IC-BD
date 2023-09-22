import pandas as pd

from dcd.tools.dataset_operations import DatasetOps
from dcd.interfaces.dc import IDC
import random

def gen_noisy_df(dc: IDC, df_ref: pd.DataFrame, noisy_percentage: float) -> pd.DataFrame:
  df = df_ref.copy()
  dfc = df.copy()

  num_tuples = df.shape[0]

  desired_noisy_qtd = int(num_tuples * (noisy_percentage / 100))
  noisy_range_error = (desired_noisy_qtd * 0.05)

  num_violations = len(DatasetOps.tuples_on_violations(df, dc))
  
  print("Desired_noisy: ", desired_noisy_qtd)

  for _ in range(10000):
    if (num_violations > desired_noisy_qtd - noisy_range_error):
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

        dfc.at[idx1, col_name_A] = dfc.at[idx2, col_name_B]
        vio_qtd_dfc = len(DatasetOps.tuples_on_violations(dfc, dc))

        print(vio_qtd_dfc)

        if vio_qtd_dfc > num_violations and vio_qtd_dfc < (desired_noisy_qtd + noisy_range_error):
          df = dfc.copy()
          num_violations = vio_qtd_dfc
        else:
          dfc = df.copy()

  return df.copy()