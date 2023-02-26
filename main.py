import os

from inmet.getStationsInformations import GetStationsInformations


class PluviometricDataScraping:
    def __init__(self) -> None:
        self.project_folder = os.path.dirname(__file__)
        self.worksheets_folder = f"{self.project_folder}/worksheets"
        
        self.__download_stations_informations()

    def __download_stations_informations(self) -> None:
        GetStationsInformations(stations_folder=self.worksheets_folder)


if __name__ == "__main__":
    PluviometricDataScraping()


