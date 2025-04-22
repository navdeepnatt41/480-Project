import psycopg2 as ps

def create_conn_cursor():
    with open("../resources/PostgreSQL_Login.txt", 'r') as f:
        dbname = f.readline().strip()
        user = f.readline().strip()
    conn = ps.connect(f"dbname={dbname} user={user}")
    return conn, conn.cursor()

