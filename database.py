import psycopg2
import os

class InitializeDb:
    """ This class sets up database connection and creates tables """

    def __init__(self, db_url):
        self.env = db_url

    @classmethod
    def init_db(cls, db_url):
        try:
            cls.connection = psycopg2.connect(db_url)
            cls.cursor = cls.connection.cursor()
            print(f'A connection to {db_url} database was established!')
        except:
            print(f'A problem occured while connecting to {db_url}')
    
    def create_tables(self):
        """ This method creates tables """

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test_users (
                id serial PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS test_address (
                id serial PRIMARY KEY NOT NULL,
                home_address TEXT NOT NULL,
                office_address TEXT NOT NULL
            );
            """
        )

        self.connection.commit()
        
    def fetch_all(self, query):
        """ This method fetches all items """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()