import os

from scripts.helpers.folderOperations import CreateFolders
from scripts.inmet.insertStationsInDB import InsertStationsInDB
from scripts.inmet.insertRainfallDataInDB import InsertRainfallDataInDB
from scripts.inmet.getStationsInformations import GetStationsInformations
from scripts.inmet.downloadAnnualRainfallData import DownloadAnnualRainfallData


class PluviometricDataScraping:
    def __init__(self, year_of_interest:str) -> None:
        self.year_of_interest = year_of_interest
        self.project_folder = os.path.dirname(__file__)
        self.worksheets_folder = f"{self.project_folder}/worksheets"

        self.stations_folder = f"{self.worksheets_folder}/stations"
        self.rainfall_data_folder = f"{self.worksheets_folder}/data/{year_of_interest}"

        CreateFolders(array_directories=[self.stations_folder, self.rainfall_data_folder])
        
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.user = os.getenv("USER")
        self.database = os.getenv("DATABASE")
        self.password = os.getenv("PASSWORD")

        self.__get_rainfall_data()
        

    def __download_stations_informations(self) -> None:
        GetStationsInformations(stations_folder=self.stations_folder)
        
        InsertStationsInDB(
            stations_folder=self.stations_folder, 
            database=self.database, 
            host=self.host, 
            user=self.user, 
            password=self.password,
            port=self.port
        )


    def __get_rainfall_data(self):
        DownloadAnnualRainfallData(
            dest_folder=self.rainfall_data_folder, 
            year_of_interest=self.year_of_interest
        )

        InsertRainfallDataInDB(
            host=self.host, 
            user=self.user, 
            port=self.port,
            database=self.database, 
            password=self.password,
            folder=self.rainfall_data_folder,
            year_of_interest=self.year_of_interest,
        )

    
if __name__ == "__main__":
    PluviometricDataScraping(year_of_interest="2023")
