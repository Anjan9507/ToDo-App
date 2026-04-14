from psycopg2.pool import SimpleConnectionPool
from backend.config import DB_URL

pool = SimpleConnectionPool(
    1, 10,
    dsn=DB_URL
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

        