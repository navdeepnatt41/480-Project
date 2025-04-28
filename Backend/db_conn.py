"""
This file is responsible for creating and returning the connection to the postgres DB with all of the tables
"""

import psycopg2 as ps

conn = ps.connect(database="taxi_db", user="postgres")

def run_sql(sql: str, vals: list, is_crud: bool): 
  with conn:
    with conn.cursor() as curs:
      try:
        curs.execute(sql, vals)
        if not is_crud:
          ret: list[tuple] = curs.fetchall()
          conn.commit()
          return ret
        else:
          conn.commit()
      except ps.Error as e:
        print("Error Occurred: " + e)
        conn.rollback()

def kill_conn() -> None:
  conn.close()

if __name__ == "__main__":
  while True:
    match input("CRUD OR NAH"):
      case "CRUD":
        print(run_sql(input(), [], is_crud=True))
      case "NAH":
        print(run_sql(input(), [], is_crud=False))