from loguru import logger
import psycopg2


class Database:

    def __init__(self, config):
        self.host = config["DATABASE_HOST"]
        self.username = config["DATABASE_USERNAME"]
        self.password = config["DATABASE_PASSWORD"]
        self.port = config["DATABASE_PORT"]
        self.dbname = config["DATABASE_NAME"]
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

newDict = {
    'DATABASE_HOST': "localhost",
    "DATABASE_USERNAME": "postgres",
    "DATABASE_PASSWORD": "aahaNoob63",
    "DATABASE_PORT": 5432,
    "DATABASE_NAME": "first_psycopg2"
}
db = Database(newDict);
db.connect();
