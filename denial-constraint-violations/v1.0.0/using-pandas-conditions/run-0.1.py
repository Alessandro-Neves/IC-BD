import pandas
from functools import reduce
import re

df = pandas.read_csv('db-a.csv')
df_mirror = df

with open('constraints.txt', 'r') as file:
  first_line = file.readline().strip()

constraints = first_line.split(',')

def get_col_name(alias, constraint):
  pattern = re.escape(alias) + r'\.(\w+)'
  correspondences = re.findall(pattern, constraint)
  if correspondences:
      return correspondences[0]
  return None

def switch_t1_by_scalar(constraint, value):
  pattern = r't1\.\w+'
  new_expression = re.sub(pattern, str(value), constraint)
  return new_expression

def resolve_left_side_constraints(df_tuple, constraints):
  lcs = []
  for cs in constraints:
    t1_col_name = get_col_name('t1', cs)
    t1_value = df_tuple[t1_col_name]
    new_cs = switch_t1_by_scalar(cs, t1_value)
    lcs.append(new_cs)

  return lcs

def to_number_else_str(input_string):
  if input_string.isdigit() or (input_string[0] == '-' and input_string[1:].isdigit()):
    return int(input_string)
  else:
    return input_string

operators_fn = {
  '>': lambda scalar, df, col: scalar > df[col],
  '<': lambda scalar, df, col: scalar < df[col],
  '=': lambda scalar, df, col: scalar == df[col],
  '>=': lambda scalar, df, col: scalar >= df[col],
  '<=': lambda scalar, df, col: scalar <= df[col],
  '<>': lambda scalar, df, col: scalar != df[col],
}

def gen_pandas_condition(df, lcs):
    
  scalar = to_number_else_str(lcs.split(' ')[0])
  operator = lcs.split(' ')[1]
  col = get_col_name('t2', lcs)

  return operators_fn[operator](scalar, df, col)

tuples_qtd = df.shape[0]


df['violations'] = 0
df['targets'] = [[] for _ in range(tuples_qtd)]

for idx, line in df.iterrows():
  left_resolved_constraints = resolve_left_side_constraints(line, constraints)
  pandas_conditions = [ gen_pandas_condition(df, lcs) for lcs in left_resolved_constraints ]
  pandas_conditions_set = reduce(lambda x, y: x & y, pandas_conditions)
  violations_ids = df[pandas_conditions_set]['id'].to_list()
  df.at[idx, 'violations'] = len(violations_ids)
  df.at[idx, 'targets'] = violations_ids

print(df)