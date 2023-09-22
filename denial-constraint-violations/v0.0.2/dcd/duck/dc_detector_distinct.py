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
      
    return pairs
  
  def __dc_predicates_to_SQL_query(self, dc: IDC):
    
    scalar_predicates = list(filter(lambda p: not p.is_relational, dc.get_predicates()))
    relational_predicates = [p for p in dc.get_predicates() if p not in scalar_predicates]
    
    same_targets_rps = list(filter(lambda p: not p.has_diff_target, relational_predicates))
    diff_targets_rps = [p for p in relational_predicates if p not in same_targets_rps]
    
    sql_query = "SELECT DISTINCT t1._id_ as _id1_, t2._id_ as _id2_ FROM T AS t1, T AS t2 WHERE"

    use_AND_clause = False
    
    if bool(diff_targets_rps):
      for rps in diff_targets_rps:
        if use_AND_clause:
          sql_query += " AND"
        use_AND_clause = True
        sql_query += f" t1.{rps.left_side.col_name_or_value} {rps.operator.value} t2.{rps.right_side.col_name_or_value}"

    if bool(same_targets_rps):
      for rps in same_targets_rps:
        if use_AND_clause:
          sql_query += " AND"
        use_AND_clause = True
        sql_query += f" t1.{rps.left_side.col_name_or_value} {rps.operator.value} t1.{rps.right_side.col_name_or_value}"

    if bool(scalar_predicates):
      for sps in scalar_predicates:
        if use_AND_clause:
          sql_query += " AND"
        use_AND_clause = True
        sql_query += f" t1.{sps.left_side.col_name_or_value} {sps.operator.value} {sps.right_side.col_name_or_value}"
    
    # sql_query += " AND t1.id <> t2.id"

    sql_query += ";"

    print(sql_query)

    return sql_query
    