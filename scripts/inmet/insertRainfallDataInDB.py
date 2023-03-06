import os
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from scripts.services.database import DataBase
from scripts.helpers.folderOperations import CreateFolders
from scripts.inmet.getAnnualRainfallDataFromCSV import GetAnnualRainfallDataFromCSV


class InsertRainfallDataInDB:
    def __init__(
            self, 
            host:str, 
            port:str,
            user:str,
            database:str, 
            password:str,
            folder:str,
            year_of_interest:str
            ) -> None:
        
        self.folder = folder
        self.year_of_interest = year_of_interest
        self.rainfall_data_folder = f"{self.folder}/rainfall_data_{self.year_of_interest}"

        CreateFolders(array_directories=[self.rainfall_data_folder])

        self.database = DataBase(
            database=database, 
            port=port, 
            host=host, 
            password=password, 
            user=user
        )

        self.__unzip()
        self.__insert_data_into_database()


    def __insert_data_into_database(self) -> pd.DataFrame:
        dataframe = self.__get_rainfall_dataframe()
        self.database._insert_dataframe_into_table(dataframe=dataframe, table_name="rainfall_data")
        

    def __get_rainfall_dataframe(self) -> pd.DataFrame:
        new_dataframe = pd.DataFrame()

        for csv_file in os.listdir(path=self.rainfall_data_folder):
            if self.__is_csv_file(csv_file=csv_file):
                station = Path(csv_file).stem
                print(f"Getting rainfall data from {station} ")
                rainfall_dataframe = GetAnnualRainfallDataFromCSV(
                    folder=self.rainfall_data_folder, 
                    filename=csv_file
                )._rainfall_dataframe()

                new_dataframe = pd.concat([new_dataframe, rainfall_dataframe], ignore_index=True)
        
        return new_dataframe
    

    def __is_csv_file(self, csv_file:str) -> bool:
        file_extension = csv_file[-4:]
        if (file_extension == ".csv") | (file_extension == ".CSV"):
            return True
        else:
            return False


    def __unzip(self) -> None:
        with ZipFile(f"{self.folder}/rainfall_data_{self.year_of_interest}.zip", "r") as zip_ref:
            zip_ref.extractall(self.rainfall_data_folder)
            zip_ref.close()
