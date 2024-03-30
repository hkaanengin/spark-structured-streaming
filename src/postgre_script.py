import psycopg2
import os
#from dotenv import load_dotenv

DB_CREDENTIALS_ENV = "env-variables/.db-credentials.env"

APP_ROOT = os.path.join(os.path.dirname(__file__))
DB_CREDENTIALS_PATH = os.path.join(APP_ROOT, DB_CREDENTIALS_ENV)


class PostgreActions:
    def __init__(self) -> None:
        #load_dotenv(DB_CREDENTIALS_ENV)
        self.conn = psycopg2.connect(f"host={os.getenv('host')} dbname={os.getenv('dbname')} user={os.getenv('user')} password={os.getenv('password')}")
        self.cur = self.conn.cursor()
    
    def get_cur(self):
        return self.conn.cursor()
    
    def create_citizen_table(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS citizen_info (
                    person_id VARCHAR(255) PRIMARY KEY,
                    citizen_name VARCHAR(255),
                    age INTEGER,
                    email VARCHAR(255),
                    address VARCHAR(255),
                    city VARCHAR(255),
                    country VARCHAR(255),
                    longitute VARCHAR(255),
                    latitude VARCHAR(255),
                    p_date VARCHAR(255),
                    p_hour VARCHAR(255)
                )
            """
        )