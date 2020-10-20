from loguru import logger
import psycopg2

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
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
            cur.close()
            return records

    def create_tables(self,query):
        """ create tables in the Postgres database"""


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

    def insert(self,user_id,user_name,password,user_email):
        try:
            cursor = self.conn.cursor()
            insert_query = """ INSERT INTO users (user_id, user_name, password, user_email) VALUES (%s,%s,%s,%s)"""
            data = (user_id, user_name, password, user_email)
            cursor.execute(insert_query, data)

            self.conn.commit()
            count = cursor.rowcount
            logger.success("Registered successfully")

        except (Exception, psycopg2.Error) as error :
            if(self.conn):
                print("Failed to insert record into users", error)

    def update(self,user_id,user_detail,key):
        try:
            cursor = self.conn.cursor()
            if(key==1):
                update_query = """ Update users set user_name = %s where user_id = %s """
                data = (user_detail,user_id)
            elif(key==2):
                update_query = """ Update users set password = %s where user_id = %s """
                data = (user_detail,user_id)
            else:
                update_query = """ Update users set user_email = %s where user_id = %s """
                data = ("user_email",user_detail,user_id)

            cursor.execute(update_query, data)

            self.conn.commit()
            count = cursor.rowcount
            logger.info("Updated successfully")

        except (Exception, psycopg2.Error) as error :
            if(self.conn):
                print("Failed to update record into users", error)

    def delete(self,id):
        try:
            cursor = self.conn.cursor()
            delete_query = """Delete from users where user_id = %s"""
            cursor.execute(delete_query, (id, ))

            self.conn.commit()
            count = cursor.rowcount
            logger.info(count, "Record deleted successfully ")

        except (Exception, psycopg2.Error) as error :
            if(self.conn):
                print("Failed to delete record from users. Error:", error)

    def close_Connection(self):
        if self.conn:
            self.conn.close()
            logger.info('Database connection closed.')


    def run_query(self, query,data):
        try:
            with self.conn.cursor() as cur:
                if 'SELECT' in query:
                    records = []
                    cur.execute(query,data)
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                else:
                    result = cur.execute(query)
                    self.conn.commit()
                    affected = f"{cur.rowcount} rows affected."
                    cur.close()
                    return affected
        except psycopg2.DatabaseError as e:
            print(e)
