import pandas
import time

dataset_a = pandas.read_csv('db-a.csv')
dataset_b = pandas.read_csv('db-b.csv')
dataset_c = pandas.read_csv('db-c.csv')

denial_constraint_violation = lambda t1, t2: t1['salario'] > t2['salario']

# Relational Product Based
def worst_method(dataset):
  tuples_qtd = dataset.shape[0]

  violations = []

  init_time = time.time()

  for t1_idx in range(tuples_qtd):
    for t2_idx in range(t1_idx, tuples_qtd):
      t1 = dataset.iloc[t1_idx]
      t2 = dataset.iloc[t2_idx]
      if denial_constraint_violation(t1, t2):
        violations.append((t1['id'], t2['id']))

  end_time = time.time()
  time_to_exec = end_time - init_time

  return (time_to_exec, violations)

# Selection Sort for based
def better_method(dataset):
  tuples_qtd = dataset.shape[0]
  
  violations = []

  init_time = time.time()

  for t1_idx in range(tuples_qtd):
    for t2_idx in range(t1_idx + 1, tuples_qtd):
      t1 = dataset.iloc[t1_idx]
      t2 = dataset.iloc[t2_idx]
      if denial_constraint_violation(t1, t2):
        violations.append((t1['id'], t2['id']))

  end_time = time.time()
  time_to_exec = end_time - init_time

  return (time_to_exec, violations)

datasets = [dataset_a, dataset_b, dataset_c]
methods = [better_method, worst_method]

results = [[], []]

for idx, dataset in enumerate(datasets):
  results[0].append(better_method(dataset)[0])
  results[1].append(worst_method(dataset)[0])

print(results)
