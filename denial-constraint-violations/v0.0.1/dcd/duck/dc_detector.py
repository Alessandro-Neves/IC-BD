from pandas import DataFrame
import duckdb
from typing import List
from functools import reduce

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector
from dcd.types.predicate import Predicate, PREDICATE_OPERATOR, get_PREDICATE_OPERATOR_by_key
from dcd.types.common import AdjacencyList

class DCDetector(IDCDetector):
  
  def find_violations(self, df: DataFrame, dc: IDC) -> AdjacencyList:    
    # con = duckdb.connect(database=':memory:') # type: ignore
    # con.register('T', df)
    
    # violations = con.execute("""
    #   SELECT t1.id, GROUP_CONCAT(t2.id) as grouped_ids
    #   FROM 
    #     T t1 
    #   JOIN 
    #     T t2 
    #   ON 
    #     t1.duration_ms = t2.duration_ms 
    #   AND
    #     t1.danceability = t1.energy
    #   GROUP BY t1.id;
    # """).df()
    
    # violations = con.execute("""
    #   SELECT t1.id, GROUP_CONCAT(t2.id) as grouped_ids
    #   FROM 
    #     T t1 
    #   JOIN 
    #     T t2 
    #   ON 
    #     t1.duration_ms = t2.duration_ms 
    #   AND
    #     t1.id <> t2.id
    #   WHERE
    #     t1.duration_ms > 10000000
    #   GROUP BY t1.id;
    # """).df()
    
    sql_query = self.__dc_predicates_to_SQL_query(dc)
    
    # return []
    
    con = duckdb.connect(database=':memory:') # type: ignore
    con.register('T', df)
    violations = con.execute(sql_query).df()
    con.close()
    
    # sourcery skip: inline-immediately-returned-variable
    adjacency_list = [
      (int(t['id']), [int(x) for x in t['grouped_ids'].split(',')]) 
      for i , t in violations.iterrows()
    ]
    
    return adjacency_list
  
  def __dc_predicates_to_SQL_query(self, dc: IDC):
    scalar_predicates = list(filter(lambda p: not p.is_relational, dc.get_predicates()))
    relational_predicates = [p for p in dc.get_predicates() if p not in scalar_predicates]
    
    used_ON_clause = False
    used_WHERE_clause = False
    
    same_targets_rps = list(filter(lambda p: not p.has_diff_target, relational_predicates))
    diff_targets_rps = [p for p in relational_predicates if p not in same_targets_rps]
    
    sql_query = "SELECT t1.id, GROUP_CONCAT(t2.id) as grouped_ids FROM T t1 JOIN T t2"
    
    if not bool(relational_predicates):
      sql_query += " ON t1.id = t2.id"

    if bool(diff_targets_rps):
      for rps in diff_targets_rps:
        if not used_ON_clause:
          sql_query += f" ON t1.{rps.left_side.col_name_or_value} {rps.operator.value} t2.{rps.right_side.col_name_or_value}"
          used_ON_clause = True
        else:
          sql_query += f" AND t1.{rps.left_side.col_name_or_value} {rps.operator.value} t2.{rps.right_side.col_name_or_value}"

    if bool(same_targets_rps):
      for rps in same_targets_rps:
        if not used_WHERE_clause:
          sql_query += f" WHERE t1.{rps.left_side.col_name_or_value} {rps.operator.value} t1.{rps.right_side.col_name_or_value}"
          used_WHERE_clause = True
        else:
          sql_query += f" AND t1.{rps.left_side.col_name_or_value} {rps.operator.value} t1.{rps.right_side.col_name_or_value}"

    if bool(scalar_predicates):
      for sps in scalar_predicates:
        if not used_WHERE_clause:
          sql_query += f" WHERE t1.{sps.left_side.col_name_or_value} {sps.operator.value} {sps.right_side.col_name_or_value}"
          used_WHERE_clause = True
        else:
          sql_query += f" AND t1.{sps.left_side.col_name_or_value} {sps.operator.value} {sps.right_side.col_name_or_value}"

    if not bool(scalar_predicates) and not bool (same_targets_rps):
          sql_query += " AND t1.id <> t2.id"

    sql_query += " GROUP BY t1.id;"

    print()
    print(sql_query, end="\n\n")

    return sql_query