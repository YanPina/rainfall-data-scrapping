import os
import pandas as pd

from scripts.inmet.getRainfallDataFromCSV import GetDataFromCSV


class InsertRainfallDataInDB:
    def __init__(self, folder:str) -> None:
        self.folder = folder

        self.__insert_data()


    def __insert_data(self) -> pd.DataFrame:
        new_dataframe = pd.DataFrame()

        for csv_file in os.listdir(path=self.folder):
            if self.__is_csv_file(csv_file=csv_file):
            
                rainfall_dataframe = GetDataFromCSV(folder=self.folder, filename=csv_file)._rainfall_dataframe()

                new_dataframe = pd.concat([new_dataframe, rainfall_dataframe], ignore_index=True)
        
        new_dataframe.to_excel(f"{self.folder}/result.xlsx")
        print(new_dataframe)
    

    def __is_csv_file(self, csv_file:str) -> bool:
        file_extension = csv_file[-4:]
        if (file_extension == ".csv") | (file_extension == ".CSV"):
            return True
        else:
            return False
        

if __name__ == "__main__":
    folder = "/Users/yanpina/Downloads/2023"
    InsertRainfallDataInDB(folder)
