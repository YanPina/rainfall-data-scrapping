import pandas as pd

import psycopg2
import psycopg2.extras as extras
from sqlalchemy import create_engine

class DataBase:

    def __init__(self, database:str, user:str, password:str, host:str, port:str):
        self.host = host
        self.port = port
        self.user = user
        self.database = database
        self.password = password

        self.connection = self.__connection()


    def __connection(self):
        return psycopg2.connect(
            database=self.database, 
            user=self.user, 
            password=self.password, 
            host=self.host, 
            port=self.port
        )


    def _insert_df_in_existing_table(self, dataframe:pd.DataFrame, table_name:str):
        tuples = [tuple(x) for x in dataframe.to_numpy()]
    
        cols = ','.join(list(dataframe.columns))
        
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)
        cursor = self.connection.cursor()
        
        try:
            extras.execute_values(cursor, query, tuples)
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.connection.rollback()
            cursor.close()
            return 1
        
        print("The dataframe is inserted")
        
        cursor.close()
        self.__close_connection()


    def _drop_table(self, table_name:str):
        print(f'\nDeleting table "{table_name}"...')
        
        cursor = self.connection.cursor()

        sql = f'''DROP TABLE "{table_name}"'''
        
        # Executing the query
        cursor.execute(sql)

        #Commit your changes in the database
        self.connection.commit()

        #Closing the connection
        self.__close_connection()

        print(f'---Table "{table_name}" deleted!---\n')


    def __engine(self):
        return create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

        
    def _create_table_from_df(self, dataframe:pd.DataFrame, table_name:str) -> None:
        print(f'\nInserting "{table_name}" into DataBase...')
        dataframe.to_sql(table_name, self.__engine(), index=False, if_exists='replace')

        print(f'---Table "{table_name}" inserted in DataBase---\n')


    def __close_connection(self) -> None:
        if self.connection is not None:
            self.connection.close()
