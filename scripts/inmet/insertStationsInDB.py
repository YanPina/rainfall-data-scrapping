import pandas as pd

from scripts.services.database import DataBase
from scripts.helpers.worksheetOperations import WorksheetOperations


class InsertStationsInDB:
    def __init__(
            self, 
            host:str, 
            port:str,
            user:str,
            database:str, 
            password:str, 
            worksheets_folder:str,
        ) -> None:
        
        self.worksheets_folder = worksheets_folder

        self.database = DataBase(
            database=database, 
            port=port, 
            host=host, 
            password=password, 
            user=user
        )

        self.stations_informations = self.__get_stations_informations()
        self.__insert()


    def __get_stations_informations(self) -> pd.DataFrame:
        return WorksheetOperations(
            worksheet_folder=self.worksheets_folder,
            worksheet_name="stations",
            format="xlsx"
        )._open_worksheet()
    

    def __insert(self) -> None:
        self.database._insert_df_in_existing_table(
            dataframe=self.stations_informations, 
            table_name="stations"
        )
    