import psycopg2
import logging
from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from typing import List

class Database:
    '''
    Database Access class. Class makes and maintains the database connection as well as sending and processing queries.
    '''
    def __init__(self, config:Config):
        self.logging = logging.getLogger(__name__)
        self.config = config
        self.pgconnection = None
        self.connected = False

    @property
    def Connected(self):
        return self.connected

    def Connect(self):
        '''
        Connect to database using the connection parameters in the Config class. The PostgresSQL documentation that
        keepalives are on by default, so it is save to maintain the connection.
        '''
        try:
            self.pgconnection = psycopg2.connect(database=self.config.DATABASE_DB,
                            user=self.config.DATABASE_USER,
                            password=self.config.DATABASE_PASSWD,
                            host=self.config.DATABASE_HOST,
                            port=self.config.DATABASE_PORT
                            )
            self.connected = True
        except Exception as e:
            self.logging.error(f"Unable to connnect to database ({self.config.DATABASE_HOST}:{self.config.DATABASE_PORT}): {str(e)}")
            raise e

    def __del__(self):
        if self.pgconnection and self.connected:
            self.pgconnection.close()


    def CreateDatabase(self):
        '''
        Create the database tables. Should be called on start to make sure the database exists. The SQL
        create the tables if they do not already exist.
        '''
        try:
            self.logging.info("Creating logging db tables (if needed)...")
            if not self.connected:
                self.pgconnection.connect()
            with self.pgconnection.cursor() as cur:
                cur.execute('CREATE TABLE IF NOT EXISTS info (version INT DEFAULT 1)')
                cur.execute('''CREATE TABLE IF NOT EXISTS urls (
                        url_id SERIAL PRIMARY KEY,
                        url VARCHAR(1024) UNIQUE
                    );''')
                cur.execute('''CREATE TABLE IF NOT EXISTS accesstimes (
                        entry_id SERIAL PRIMARY KEY,
                        url_id INT REFERENCES urls(url_id),
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reactiontime DOUBLE PRECISION DEFAULT 0.0,
                        success BOOLEAN DEFAULT FALSE
                    );''')
            self.pgconnection.commit()
            self.logging.info("Creating db tables complete")
        except psycopg2.Error as e:
            self.logging.error(f"Unable to create the database ({self.config.DATABASE_DB}): {str(e)}")

    def DropDatabase(self):
        '''
        Drop the database tables. Routine is not normally used, but included for testing.
        '''
        try:
            self.logging.info("Dropping logging db tables (if needed)...")
            if not self.connected:
                self.pgconnection.connect()
            with self.pgconnection.cursor() as cur:
                cur.execute('DROP TABLE IF EXISTS accesstimes;')
                cur.execute('DROP TABLE IF EXISTS urls')
                cur.execute('DROP TABLE IF EXISTS info')
            self.pgconnection.commit()
            self.logging.info("Drop db tables complete")
        except psycopg2.Error as e:
            self.logging.error(f"Unable to create the database ({self.config.DATABASE_DB}): {str(e)}")


    def InsertData(self, data:URLItem):
        '''
        Insert an data object into the database
        '''

        # Reconnect if we aren't connected or the connection dropped
        if not self.connected:
            self.pgconnection.connect()

        # This should be done in one query...
        result = None
        with self.pgconnection.cursor() as cur:
            cur.execute(f"SELECT url_id from urls where url = '{data.Url}'")
            result = cur.fetchall()
        if len(result)==0:
            with self.pgconnection.cursor() as cur:
                cur.execute(f'''WITH ins AS (
                    INSERT INTO urls
                        (url) 
                    VALUES
                        ('{data.Url}')
                    RETURNING url_id
                    )
                    INSERT INTO accesstimes 
                    (url_id, reactiontime, success)
                    SELECT
                    ins.url_id, {data.ReactionTime}, {data.Success}
                    FROM ins;'''
                )
        else:
            with self.pgconnection.cursor() as cur:
                cur.execute(f'INSERT INTO accesstimes (url_id, reactiontime, success) VALUES({result[0][0]}, {data.ReactionTime}, {data.Success})')
        self.pgconnection.commit()

    def GetData(self) -> List[URLItem]:
        pass