# """
# This file is responsible for creating and returning the connection to the postgres DB with all of the tables
# """

# import psycopg2 as ps

# conn = ps.connect(database="taxi_db", user="postgres")

# def run_sql(sql: str, vals: list, is_crud: bool): 
#   with conn:
#     with conn.cursor() as curs:
#       try:
#         curs.execute(sql, vals)
#         if (sql.startswith("DELETE")):
#           conn.commit()
#         else:
#           ret: list[tuple] = curs.fetchall()
#           conn.commit()
#           return ret
#       except ps.Error as e:
#         print("Error Occurred: " + str(e))
#         conn.rollback()

# def kill_conn() -> None:
#   conn.close()

# if __name__ == "__main__":
#   while True:
#     match input("CRUD OR NAH"):
#       case "CRUD":
#         print(run_sql(input(), [], is_crud=True))
#       case "NAH":
#         print(run_sql(input(), [], is_crud=False))


import psycopg2 as ps
from typing import Any, List, Tuple, Optional

conn = ps.connect(database="taxi_db", user="postgres")


def run_sql(
    sql: str,
    vals: Optional[List[Any]] = None,
    *,
    is_crud: bool = False,
    returning: bool = False
) -> Optional[List[Tuple]]:

    vals = vals or []

    with conn:
        with conn.cursor() as curs:
            try:
                curs.execute(sql, vals)

                if is_crud and not returning:          # plain INSERT/UPDATE/DELETE
                    conn.commit()
                    return curs.rowcount               # handy but optional

                rows = curs.fetchall()                 # SELECT or DML … RETURNING
                conn.commit()
                return rows

            except ps.ProgrammingError as e:
                # occurs when .fetchall() has no result set
                if is_crud and not returning:
                    conn.commit()
                    return curs.rowcount
                conn.rollback()
                print("Programming error:", e)

            except ps.Error as e:
                conn.rollback()
                print("Database error:", e)


def kill_conn():
    conn.close()


# quick interactive REPL for ad-hoc queries
if __name__ == "__main__":
    while True:
        try:
            q = input("sql> ")
            if q.lower() in ("quit", "exit"):
                break
            print(run_sql(q, [], is_crud=not q.strip().lower().startswith("select")))
        except (KeyboardInterrupt, EOFError):
            break
