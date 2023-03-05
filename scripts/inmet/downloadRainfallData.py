from scripts.helpers.downloadFile import DownloadFile


class DownloadRainfallData:
    def __init__(self, dest_folder:str, year_of_interest:str) -> None:
        self.year_of_interest = year_of_interest
        self.dest_folder = dest_folder

        self.url = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{year_of_interest}.zip"

        self.__download_rainfall_data()


    def __download_rainfall_data(self) -> None:
        DownloadFile(
            url=self.url, 
            format="zip",
            dest_folder=self.dest_folder, 
            filename=f"rainfall_data_{self.year_of_interest}", 
            download_message=f"Downloading rainfall data of {self.year_of_interest}"
        )
