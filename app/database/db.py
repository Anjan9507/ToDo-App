from psycopg2.pool import SimpleConnectionPool
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

pool = SimpleConnectionPool(
    1, 10,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

class DBSession:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        return self.conn.commit()
    
    def rollback(self):
        return self.conn.rollback()
    

def get_db():
    conn = pool.getconn()
    db=DBSession(conn)
    try:
        yield db
    finally:
        pool.putconn(conn)

        