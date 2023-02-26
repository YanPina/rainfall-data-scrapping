import os
import warnings
from time import sleep

import pandas as pd

from helpers.seleniumWebDriver import WebDriver
from helpers.folderOperations import CreateFolders
from helpers.checkFileDownload import CheckFileDownload
from helpers.worksheetOperations import WorksheetOperations


warnings.filterwarnings("ignore") #Remove unnecessary UserWarnings

class GetStationsInformations:
    def __init__(self, stations_folder:str) -> None:
        self.stations_folder = stations_folder
        CreateFolders(array_directories=[self.stations_folder])

        self.driver = WebDriver(
            isChangeDownloadFolder=True, 
            newDownloadFolder=self.stations_folder
        )

        self.stations = [
            {   
                'stations_type':'conventional_stations',
                'url':'https://portal.inmet.gov.br/paginas/catalogoman',
                'csv_name':'CatalogoEstaçõesConvencionais',
                'XPATH_button':'//*[@id="downloadcatalogom"]'
            },
            {
                'stations_type':'automatic_stations',
                'url':'https://portal.inmet.gov.br/paginas/catalogoaut',
                'csv_name':'CatalogoEstaçõesAutomáticas',
                'XPATH_button':'//*[@id="downloadcatalogo"]'
            }
        ]

        self.__download_stations()
        self.__generate_stations_worksheet()


    def __generate_stations_worksheet(self) -> None:
        df_stations = self.__get_df_stations()
        
        WorksheetOperations(
            dataframe=df_stations,
            dest_folder=self.stations_folder,
            worksheet_name='stations',
            format='xlsx'
        )._save_worksheet()

        print('\nStations obtained!!')


    def __get_df_stations(self) -> pd.DataFrame:
        df = pd.DataFrame()
        for station in self.stations:
            df_station = WorksheetOperations(
                worksheet_name=station['csv_name'], 
                worksheet_folder=self.stations_folder,
                format='csv'
            )._open_worksheet()
            
            df = df.append(df_station)
        
        return self.__format_columns(dataframe_stations=df)


    def __format_columns(self, dataframe_stations:pd.DataFrame) -> pd.DataFrame:
        dataframe_stations = dataframe_stations[['DC_NOME', 'SG_ESTADO', 'CD_SITUACAO', 'VL_LATITUDE', 'VL_LONGITUDE', 'CD_ESTACAO']]
        dataframe_stations['CD_ESTACAO'] = dataframe_stations['CD_ESTACAO'].astype(str)
        
        dataframe_stations = dataframe_stations.rename(columns={
            "DC_NOME": "station_name", 
            "SG_ESTADO": "initials_state", 
            "CD_SITUACAO": "status",
            "VL_LATITUDE": "latitude",
            "VL_LONGITUDE": "longitude",
            "CD_ESTACAO": "station_code"
            }
        )

        return dataframe_stations

    def __download_stations(self) -> None:
        print('\nDownloading pluviometric stations...\n')
        for station in self.stations:
            if not self.__is_worksheet_in_folder(
                worksheet_folder=self.stations_folder, 
                worksheet_name=station['csv_name'], 
                format='csv'
            ):
                self.driver._get_url(url=station['url']) 
                sleep(1)
                self.driver._click_element(element=station['XPATH_button'], find_method='XPATH')

                CheckFileDownload(
                    filename=station['csv_name'], 
                    file_folder=self.stations_folder, 
                    file_format='csv'
                )
            sleep(2)

    def __is_worksheet_in_folder(self, worksheet_folder:str, worksheet_name:str, format:str) -> bool:
        if os.path.isfile(f'{worksheet_folder}/{worksheet_name}.{format}'):
            return True
        else:
            return False
        