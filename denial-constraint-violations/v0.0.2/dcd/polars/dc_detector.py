# type: ignore
from pandas import DataFrame
import polars as pl
import copy
from typing import List
from functools import reduce
from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector
from dcd.types.predicate import Predicate, PREDICATE_OPERATOR
from dcd.types.common import PairIdList


class DCDetector(IDCDetector):
  
  def find_violations(self, df: DataFrame, dc: IDC) -> PairIdList:  
    dfp = pl.DataFrame(df)  
    
    df2 = dfp
    tuples_qtd = df2.shape[0]
    
    scalar_predicates = list(filter(lambda p: not p.is_relational, dc.get_predicates()))
    relational_predicates = [p for p in dc.get_predicates() if p not in scalar_predicates]
    
    violations = pl.DataFrame()
    
    if bool(scalar_predicates):
      violations = self.__filter_by_scalar_predicates(dfp, scalar_predicates)
      print(len(violations))
      # violations_ids = dfp.filter(pl.col("salary") < 10900) 
    
    if bool(relational_predicates):
      same_targets_rps = list(filter(lambda p: not p.has_diff_target, relational_predicates))
      diff_targets_rps = [p for p in relational_predicates if p not in same_targets_rps]
      
      targets = violations if bool(scalar_predicates) else df2
      
      if bool(same_targets_rps):
        violations = self.__filter_by_same_target_predicates(targets, dfp, same_targets_rps)
        targets = violations
        print("st", len(violations))
        print(violations)
        
      if bool(diff_targets_rps):
        violations_pairs_diff = self.__filter_by_diff_target_predicates(targets, dfp, diff_targets_rps)
        print(len(violations_pairs_diff))
    
    return []
    
    if bool(relational_predicates):
      same_targets_rps = list(filter(lambda p: not p.has_diff_target, relational_predicates))
      diff_targets_rps = [p for p in relational_predicates if p not in same_targets_rps]
      
      targets = violations if bool(scalar_predicates) else df2
      
      if bool(same_targets_rps):
        violations = self.__filter_by_same_target_predicates(targets, df, same_targets_rps)
        targets = violations
        
      if bool(diff_targets_rps):
        violations = self.__filter_by_diff_target_predicates(targets, df, diff_targets_rps)
        
    adjacency_list = [(int(t['id']), t['targets']) for i , t in violations.iterrows()] # type: ignore
    
    adjacency_list_with_some = list(filter(lambda t: bool(t[1]), adjacency_list))  # type: ignore
    
    pairs = []
    for t in adjacency_list_with_some:
      t1 = t[0]
      for t2 in t[1]:
        pairs.append(tuple((t1, t2))) # type: ignore
    return pairs
          
  def __filter_by_scalar_predicates(self, df: pl.DataFrame, scalar_predicates: List[Predicate]) -> DataFrame:
    if not bool(scalar_predicates):
      raise Exception("DCDetector::__filter_by_scalar_predicates:\nempty scalar_predicates list")
    
    operators_fn = {
      PREDICATE_OPERATOR.GT: lambda df, col, scalar: pl.col(col) > scalar,
      PREDICATE_OPERATOR.LT: lambda df, col, scalar: pl.col(col) < scalar,
      PREDICATE_OPERATOR.EQ: lambda df, col, scalar: pl.col(col) == scalar,
      PREDICATE_OPERATOR.GTE: lambda df, col, scalar: pl.col(col) >= scalar,
      PREDICATE_OPERATOR.LTE: lambda df, col, scalar: pl.col(col) <= scalar,
      PREDICATE_OPERATOR.IQ: lambda df, col, scalar: pl.col(col) != scalar,
    }
    
    for sp in scalar_predicates:
      if sp.left_side.is_scalar_value or not sp.right_side.is_scalar_value:
        raise Exception(f"DCDetector::__filter_by_scalar_predicates:\nunexpected scalar predicate\nparam: {sp}")
    
    conditions = [ operators_fn[sp.operator]
                  (df, sp.left_side.col_name_or_value, sp.right_side.col_name_or_value) 
                  for sp in scalar_predicates]
    
    res = df.filter(reduce(lambda x, y: x & y, conditions))
    
    # for i, line in res.iterrows():
    #   res.at[i, 'targets'].append(int(line['id']))
      
    return res
  
  def __filter_by_diff_target_predicates(self, targets: pl.DataFrame, df: pl.DataFrame, rel_predicates: List[Predicate]) -> DataFrame:
    
    operators_fn = {
      PREDICATE_OPERATOR.GT: lambda scalar, df, col: scalar > pl.col(col),
      PREDICATE_OPERATOR.LT: lambda scalar, df, col: scalar < pl.col(col),
      PREDICATE_OPERATOR.EQ: lambda scalar, df, col: scalar == pl.col(col),
      PREDICATE_OPERATOR.GTE: lambda scalar, df, col: scalar >= pl.col(col),
      PREDICATE_OPERATOR.LTE: lambda scalar, df, col: scalar <= pl.col(col),
      PREDICATE_OPERATOR.IQ: lambda scalar, df, col: scalar != pl.col(col),
    }
    
    violations_pairs = []
    
    for index, t in enumerate(targets.iter_rows(named=True)):
      conditions = [ operators_fn[rp.operator]
                  (t[rp.left_side.col_name_or_value], df, rp.right_side.col_name_or_value) 
                  for rp in rel_predicates]
      
      conditions.append(pl.col('id') != t['id'])
      
      
      violations_ids = df.filter(reduce(lambda x, y: x & y, conditions))['id'].to_pandas().tolist()
      
      # if not bool(violations_ids):
      #   targets = targets.filter(pl.col("id") != t['id'])
      if bool(violations_ids):
        violations_pairs.extend((t['id'], v) for v in violations_ids)
      
    return violations_pairs
  
  def __filter_by_same_target_predicates(self, targets: pl.DataFrame, df: pl.DataFrame, rel_predicates: List[Predicate]) -> DataFrame:
    operators_fn = {
      PREDICATE_OPERATOR.GT: lambda col_a, df, col_b: pl.col(col_a) > pl.col(col_b),
      PREDICATE_OPERATOR.LT: lambda col_a, df, col_b: pl.col(col_a) < pl.col(col_b),
      PREDICATE_OPERATOR.EQ: lambda col_a, df, col_b: pl.col(col_a) == pl.col(col_b),
      PREDICATE_OPERATOR.GTE: lambda col_a, df, col_b: pl.col(col_a) >= pl.col(col_b),
      PREDICATE_OPERATOR.LTE: lambda col_a, df, col_b: pl.col(col_a) <= pl.col(col_b),
      PREDICATE_OPERATOR.IQ: lambda col_a, df, col_b: pl.col(col_a) != pl.col(col_b),
    }
    
    conditions = [ operators_fn[rp.operator]
                (rp.left_side.col_name_or_value, df, rp.right_side.col_name_or_value) 
                for rp in rel_predicates]
    
    # conditions.append(df['id'].isin(targets['id']))
    conditions.append(pl.col('id').is_in(targets['id']))
    
    res = df.filter(reduce(lambda x, y: x & y, conditions))
        
    # for i, line in res.iterrows():
    #   res.at[i, 'targets'].append(int(line['id'])) # type: ignore
      
    return res