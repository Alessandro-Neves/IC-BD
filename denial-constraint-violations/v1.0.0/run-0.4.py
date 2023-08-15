import pandas
dataset = pandas.read_csv('db-a.csv')

with open('constraints.txt', 'r') as file:
  first_line = file.readline().strip()

constraints = first_line.split(',')

def split_components(predicate):
  components = predicate.split(' ')
  return {
    't1_col': components[0].split('.')[1],
    't2_col': components[2].split('.')[1],
    'operator': components[1]
  }

operators = {
  '>': lambda a, b: a > b,
  '<': lambda a, b: a < b,
  '=': lambda a, b: a == b,
  '>=': lambda a, b: a >= b,
  '<=': lambda a, b: a <= b,
  '<>': lambda a, b: a != b,
}

def constraint_to_lambda_func(constraint):
  pc = split_components(constraint)
  return lambda t1, t2: operators[pc['operator']](t1[pc['t1_col']], t2[pc['t2_col']])

constraints_validations = [ constraint_to_lambda_func(i) for i in constraints]

def violates_all_constraints(constraints_validations, t1, t2):
  for cv in constraints_validations:
    if not cv(t1, t2):
      return False
  
  return True

tuples_qtd = dataset.shape[0]

dataset['violation'] = False
dataset['target'] = [[] for _ in range(tuples_qtd)]

for t1_idx in range(tuples_qtd):
  for t2_idx in range(t1_idx + 1, tuples_qtd):
    t1 = dataset.iloc[t1_idx]
    t2 = dataset.iloc[t2_idx]
    dataset.at[t1_idx, 'violation'] = violates_all_constraints(constraints_validations, t1, t2)
    dataset.at[t2_idx, 'violation'] = violates_all_constraints(constraints_validations, t2, t1)

    if dataset.at[t1_idx, 'violation']:
      dataset.at[t1_idx, 'target'].append(t2['id'])

    if dataset.at[t2_idx, 'violation']:
      dataset.at[t2_idx, 'target'].append(t1['id'])

print(dataset)