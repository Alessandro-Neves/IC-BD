import pandas
dataset = pandas.read_csv('db-a.csv')

denial_constraint_violation = lambda t1, t2: t1['salario'] > t2['salario']

tuples_qtd = dataset.shape[0]

dataset['violation'] = False

for t1_idx in range(tuples_qtd):
  for t2_idx in range(t1_idx + 1, tuples_qtd):
    t1 = dataset.iloc[t1_idx]
    t2 = dataset.iloc[t2_idx]
    dataset.at[t1_idx, 'violation'] = True if dataset.at[t1_idx, 'violation'] or denial_constraint_violation(t1, t2) else False
    dataset.at[t2_idx, 'violation'] = True if dataset.at[t2_idx, 'violation'] or denial_constraint_violation(t2, t1) else False

print(dataset)