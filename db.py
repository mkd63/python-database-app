from loguru import logger
import psycopg2
import index

class Database:

    def __init__(self, config):
        self.host = config.DATABASE_HOST
        self.username = config.DATABASE_USERNAME
        self.password = config.DATABASE_PASSWORD
        self.port = config.DATABASE_PORT
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                logger.error(e)
                raise e
            finally:
                logger.info('Connection opened successfully.')

    def select_rows(self, query):
        """Run a SQL query to select rows from table."""
        self.open_connection()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
            cur.close()
            return records

    def create_tables(self,query):
        """ create tables in the PostgreSQL database"""


        with self.conn.cursor() as cur:
            try:
                # execute the given commands
                cur.execute(query)
                # close communication with the PostgreSQL database server
                cur.close()
                # commit the changes
                self.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                logger.info('Table added')
                if self.conn is not None:
                    self.conn.close()

db = Database(index)
db.connect()
db.create_tables(
"""
    CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            user_email VARCHAR(255) NOT NULL
        )
"""
)
