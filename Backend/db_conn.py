"""
This file is responsible for creating and returning the connection to the postgres DB with all of the tables
"""

import psycopg2 as ps

conn = ps.connect(database="taxi_db", user="postgres")

def run_sql(sql: str) -> list[tuple]:
  with conn:
    with conn.cursor() as curs:
      try:
        curs.execute(sql)
        ret: list[tuple] = curs.fetchall()
        conn.commit()
        return ret
      except ps.Error as e:
        print("Error Occurred: " + e)
        conn.rollback()
