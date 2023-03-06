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

    
    def __engine(self):
        return create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')


    def _insert_dataframe_into_table(self, dataframe:pd.DataFrame, table_name:str) -> None:
        if not self.__table_exist(table_name):
            self.__create_table_from_dataframe(table_name=table_name, dataframe=dataframe)

        print(f'\nInserting dataframe into table "{table_name}"...')

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
        
        print("The dataframe is inserted!")
        
        cursor.close()
        self.__close_connection()


    def __create_table_from_dataframe(self, table_name:str, dataframe:pd.DataFrame) -> None:
        print(f'\nInserting "{table_name}" into DataBase...')

        string_columns_query = self.__create_column_string_query(dataframe)

        query = f"""CREATE TABLE {table_name} (
            {string_columns_query}
        )"""

        try:
            cur = self.connection.cursor()
            # create table
            cur.execute(query)

            #Commit changes in the database
            self.connection.commit()

            # close communication with the PostgreSQL database server
            self.__close_connection()
            print(f'Table "{table_name}" inserted in DataBase!!')
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.__close_connection()

    
    def __create_column_string_query(self, dataframe:pd.DataFrame) -> str:
        columns_values = []

        dataframe_columns = list(dataframe.columns)
        
        for column in dataframe_columns:
            dtype_column = self.__get_column_type(str(dataframe[f"{column}"].dtype))
            query_string_column = f"{column} {dtype_column}"
            
            columns_values.append(query_string_column)
        
        query_values = ','.join(columns_values)

        return query_values
            

    def __get_column_type(self, type:str) -> str:
        return {
            "string":"TEXT",
            "int64":"INTEGER",
            "float64":"DOUBLE PRECISION"
        }[type]


    def __table_exist(self, table_name:str) -> bool:
        cur = self.connection.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", (f'{table_name}',))

        return bool(cur.rowcount)


    def _drop_table(self, table_name:str) -> None:
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


    def __close_connection(self) -> None:
        if self.connection is not None:
            self.connection.close()

