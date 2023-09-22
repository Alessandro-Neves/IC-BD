from pandas import DataFrame
import duckdb

from dcd.interfaces.dc import IDC
from dcd.interfaces.dc_detector import IDCDetector
from dcd.types.common import PairIdList

class DCDetector(IDCDetector):
  
  def find_violations(self, df: DataFrame, dc: IDC) -> PairIdList: 

    sql_query = self.__dc_predicates_to_SQL_query(dc)
    
    con = duckdb.connect(database=':memory:') # type: ignore
    con.register('T', df)
    violations = con.execute(sql_query).df()
    con.close()
    
    pairs = []
    for i, t in violations.iterrows():
      pairs.append((int(t['_id1_']), int(t['_id2_'])))
      
      
    # print(sql_query)
    # print(pairs[0])
    
    return pairs
  
  def __dc_predicates_to_SQL_query(self, dc: IDC):
    # return """
    # SELECT t1._id_ as id1, t2._id_ as id2
    # FROM T t1
    # JOIN T t2 ON t1.salary > t2.salary AND t1.hiring_year > t2.hiring_year AND t1.salary > 37800;
    # """
    scalar_predicates = list(filter(lambda p: not p.is_relational, dc.get_predicates()))
    relational_predicates = [p for p in dc.get_predicates() if p not in scalar_predicates]
    
    used_ON_clause = False
    used_WHERE_clause = False
    
    same_targets_rps = list(filter(lambda p: not p.has_diff_target, relational_predicates))
    diff_targets_rps = [p for p in relational_predicates if p not in same_targets_rps]
    
    sql_query = "SELECT t1._id_ as _id1_, t2._id_ as _id2_ FROM T t1 JOIN T t2"
    
    if not bool(diff_targets_rps):
      sql_query += " ON t1._id_ = t2._id_"

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

    if not bool(scalar_predicates) and not bool(same_targets_rps):
          sql_query += " AND t1._id_ <> t2._id_"

    sql_query += ";"

    # print(sql_query)

    return sql_query