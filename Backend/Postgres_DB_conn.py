import psycopg2 as ps

def create_conn_cursor() ->  ps.cursor:
    """
    Creates a connection to the PostgreSQL DB and returns a cursor

    return: pyscopg2.cursor 
    """
    # We're too cool to use try-catch 😎
    with open("../resources/PostgreSQL_Login.txt", 'r') as f:
        dbname: str = f.readline()
        user: str = f.readline()
    conn = ps.connect(f"dbname={dbname} user={user}")
    return conn.cursor() 
        
