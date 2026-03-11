import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv


load_dotenv()


db_pool = None

def init_db_pool():
    global db_pool
    if db_pool is None:
        try:
            db_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="gated_community_pool",
                pool_size=5,
                pool_reset_session=True,
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "3306"),
                database=os.getenv("DB_NAME", "gated_community_db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "")
            )
            print("Database connection pool initialized successfully.")
        except mysql.connector.Error as err:
            print(f"Error initializing connection pool: {err}")
            raise err

def get_db_connection():
   
    if db_pool is None:
        init_db_pool()
    return db_pool.get_connection()

if __name__ == "__main__":
   
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("Successfully connected to the database.")
        conn.close()
    except Exception as e:
        print(f"Connection test failed: {e}")
