import pandas
from functools import reduce
import re

def check_constraint_sintax(constraint):
    pattern1 = r"t1\..*\s+[<>=!]+\s+t2\..*"
    pattern2 = r"t1\..*\s+[<>=!]+\s+(?:\d+|\'.*\'|\".*\")"          # TODO: retirar t1.* right side 

    if re.match(pattern1, constraint) or re.match(pattern2, constraint):
        return True
    else:
        print(f"invalid constraint sintax: {constraint}")
        exit(0)
    
def has_scalar_value_compare(constraint):
    pattern = r"t1\..*\s+[<>=!]+\s+t2\..*"
    return False if re.match(pattern, constraint) else True

def to_number_else_str(input_string):
    if input_string.isdigit() or (input_string[0] == '-' and input_string[1:].isdigit()):
        return int(input_string)
    else:
        return input_string

def get_col_name(alias, constraint):
    pattern = re.escape(alias) + r'\.(\w+)'
    correspondences = re.findall(pattern, constraint)
    if correspondences:
        return correspondences[0]
    return None

operators_fn = {
  '>': lambda scalar, df, col: scalar > df[col],
  '<': lambda scalar, df, col: scalar < df[col],
  '=': lambda scalar, df, col: scalar == df[col],
  '>=': lambda scalar, df, col: scalar >= df[col],
  '<=': lambda scalar, df, col: scalar <= df[col],
  '<>': lambda scalar, df, col: scalar != df[col],
}

def gen_pandas_condition(df, lcs, col_alias):
    
    scalar = to_number_else_str(lcs.split(' ')[0])
    operator = lcs.split(' ')[1]
    col = get_col_name(col_alias, lcs)

    return operators_fn[operator](scalar, df, col)

def invert_expression(expression):
    operators = {
        '<': '>',
        '>': '<',
        '<=': '>=',
        '>=': '<=',
        '!=': '!=',
        '=': '='
    }

    pattern = r'(t1\.\w+)\s*([><=]+)\s*(\d+)'

    substitution = lambda match: f'{match.group(3)} {operators.get(match.group(2), match.group(2))} {match.group(1)}'

    new_expression = re.sub(pattern, substitution, expression)
    return new_expression

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

########################## EXEC ##########################

df = pandas.read_csv('db-a.csv')

with open('constraints.txt', 'r') as file:
    first_line = file.readline().strip()

constraints = first_line.split(',')

for cs in constraints:
  check_constraint_sintax(cs)

scalar_constraints = list(filter(has_scalar_value_compare, constraints))
relational_constraints = [cs for cs in constraints if cs not in scalar_constraints]

df_filtered_by_scalar_ex = df

if len(scalar_constraints):
  constraints_scalar_left_side = [ invert_expression(sc) for sc in  scalar_constraints]
  pandas_scalar_conditions = [ gen_pandas_condition(df, csl, 't1') for csl in constraints_scalar_left_side ]
  df_filtered_by_scalar_ex = df[reduce(lambda x, y: x & y, pandas_scalar_conditions)]

tuples_qtd = df.shape[0]

df['violations'] = 0
df['targets'] = [[] for _ in range(tuples_qtd)]

if bool(len(relational_constraints)):
  for idx, line in df_filtered_by_scalar_ex.iterrows():
    left_resolved_constraints = resolve_left_side_constraints(line, relational_constraints)
    pandas_conditions = [ gen_pandas_condition(df, lcs, 't2') for lcs in left_resolved_constraints ]
    pandas_conditions_set = reduce(lambda x, y: x & y, pandas_conditions)
    violations_ids = df[pandas_conditions_set]['id'].to_list()
    df.at[idx, 'violations'] = len(violations_ids)
    df.at[idx, 'targets'] = violations_ids

else:
  for idx, line in df_filtered_by_scalar_ex.iterrows():
    df.at[idx, 'violations'] = 1
    df.at[idx, 'targets'] = [line['id']]

print(constraints, end='\n\n')
print(df)