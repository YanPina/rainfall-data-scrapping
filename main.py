import os

from scripts.inmet.insertStationsInDB import InsertStationsInDB
from scripts.inmet.downloadRainfallData import DownloadRainfallData
from scripts.inmet.getStationsInformations import GetStationsInformations

class PluviometricDataScraping:
    def __init__(self, year_of_interest:str) -> None:
        self.year_of_interest = year_of_interest
        self.project_folder = os.path.dirname(__file__)
        self.worksheets_folder = f"{self.project_folder}/worksheets"

        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.user = os.getenv("USER")
        self.database = os.getenv("DATABASE")
        self.password = os.getenv("PASSWORD")
        
        self.__download_stations_informations()


    def __download_stations_informations(self) -> None:
        GetStationsInformations(stations_folder=self.worksheets_folder)
        
        InsertStationsInDB(
            worksheets_folder=self.worksheets_folder, 
            database=self.database, 
            host=self.host, 
            user=self.user, 
            password=self.password,
            port=self.port
        )

        DownloadRainfallData(
            dest_folder=self.worksheets_folder, 
            year_of_interest=self.year_of_interest
        )

    
if __name__ == "__main__":
    PluviometricDataScraping(year_of_interest="2023")
