import csv

import numpy as np
import pandas as pd


class GetAnnualRainfallDataFromCSV:
    def __init__(self, folder:str, filename:str) -> None:
        self.folder = folder
        self.filename = filename

        self.code_station:str=""
        self.data:list=[]
        self.hora_utc:list=[]
        self.precipitao_total_horario_mm:list=[]
        self.pressao_atmosferica_ao_nivel_da_estacao_horaria_mb:list=[]
        self.pressao_atmosferica_max_na_hora_ant_aut_mb:list=[]
        self.pressao_atmosferica_min_na_hora_ant_aut_mb:list=[]
        self.radiacao_global_kjm:list=[]
        self.temperatura_do_ar_bulbo_seco_horaria_c:list=[]
        self.temperatura_do_ponto_de_orvalho_c:list=[]
        self.temperatura_maxima_na_hora_ant_aut_c:list=[]
        self.temperatura_minima_na_hora_ant_aut_c:list=[]
        self.temperatura_orvalho_max_na_hora_ant_aut_c:list=[]
        self.temperatura_orvalho_min_na_hora_ant_aut_c:list=[]
        self.umidade_rel_max_na_hora_ant_aut:list=[]
        self.umidade_rel_min_na_hora_ant_aut:list=[]
        self.umidade_relativa_do_ar_horaria:list=[]
        self.vento_direcao_horaria_gr:list=[]
        self.vento_rajada_maxima_ms:list=[]
        self.vento_velocidade_horaria_ms:list=[]

        self.__get_data()


    def __get_data(self) -> pd.DataFrame:
        count = 0
        with open(f"{self.folder}/{self.filename}", newline="", errors="ignore") as csvfile:
            data = csv.reader(csvfile, delimiter=';')

            for row in data:
                row_code_station = str(row[0])[0:6]
                
                if row_code_station == "CODIGO":
                    self.code_station = str(row[1])

                if count > 8:
                    self.data.append(row[0])
                    self.hora_utc.append(row[1])
                    self.precipitao_total_horario_mm.append(self.__improve_number_data(row[2]))
                    self.pressao_atmosferica_ao_nivel_da_estacao_horaria_mb.append(self.__improve_number_data(row[3]))
                    self.pressao_atmosferica_max_na_hora_ant_aut_mb.append(self.__improve_number_data(row[4]))
                    self.pressao_atmosferica_min_na_hora_ant_aut_mb.append(self.__improve_number_data(row[5]))
                    self.radiacao_global_kjm.append(self.__improve_number_data(row[6]))
                    self.temperatura_do_ar_bulbo_seco_horaria_c.append(self.__improve_number_data(row[7]))
                    self.temperatura_do_ponto_de_orvalho_c.append(self.__improve_number_data(row[8]))
                    self.temperatura_maxima_na_hora_ant_aut_c.append(self.__improve_number_data(row[9]))
                    self.temperatura_minima_na_hora_ant_aut_c.append(self.__improve_number_data(row[10]))
                    self.temperatura_orvalho_max_na_hora_ant_aut_c.append(self.__improve_number_data(row[11]))
                    self.temperatura_orvalho_min_na_hora_ant_aut_c.append(self.__improve_number_data(row[12]))
                    self.umidade_rel_max_na_hora_ant_aut.append(self.__improve_number_data(row[13]))
                    self.umidade_rel_min_na_hora_ant_aut.append(self.__improve_number_data(row[14]))
                    self.umidade_relativa_do_ar_horaria.append(self.__improve_number_data(row[15]))
                    self.vento_direcao_horaria_gr.append(self.__improve_number_data(row[16]))
                    self.vento_rajada_maxima_ms.append(self.__improve_number_data(row[17]))
                    self.vento_velocidade_horaria_ms.append(self.__improve_number_data(row[18]))
                    
                count = count + 1


    def _rainfall_dataframe(self) -> pd.DataFrame:
        dict_data = self.__dict_data()

        data = pd.DataFrame(data=dict_data)

        data["station_code"] = self.code_station
        
        data = self.__format_columns(dataframe=data)

        return data
    

    def __format_columns(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
        dataframe = self.__columns_to_float(dataframe=dataframe)

        dataframe["hora_utc"] = dataframe["hora_utc"].str[:2].astype(int)

        dataframe["data"] = dataframe["data"].str.replace("/", "").astype(int)
        dataframe["station_code"] = dataframe["station_code"].astype("string")

        return dataframe
    
  
    def __columns_to_float(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        
        
        columns_to_float = [
            "precipitao_total_horario_mm",
            "pressao_atmosferica_ao_nivel_da_estacao_horaria_mb",
            "pressao_atmosferica_max_na_hora_ant_aut_mb",
            "pressao_atmosferica_min_na_hora_ant_aut_mb",
            "radiacao_global_kjm",
            "temperatura_do_ar_bulbo_seco_horaria_c",
            "temperatura_do_ponto_de_orvalho_c",
            "temperatura_maxima_na_hora_ant_aut_c",
            "temperatura_minima_na_hora_ant_aut_c",
            "temperatura_orvalho_max_na_hora_ant_aut_c",
            "temperatura_orvalho_min_na_hora_ant_aut_c",
            "umidade_rel_max_na_hora_ant_aut",
            "umidade_rel_min_na_hora_ant_aut",
            "umidade_relativa_do_ar_horaria",
            "vento_direcao_horaria_gr",
            "vento_rajada_maxima_ms",
            "vento_velocidade_horaria_ms"
        ]

        for column in columns_to_float:
            dataframe[f"{column}"] = dataframe[f"{column}"].astype(float)

        return dataframe
    
    def __improve_number_data(self, row_data:str) -> float | str:
        if row_data != "":
            row_data = self.__add_zero(row_data=row_data)

            improved_data = row_data.replace(",", ".")

            return float(improved_data)
        else:
            return row_data
        
    
    def __add_zero(self, row_data:str) -> str:
        if row_data[0] == ",":
            row_data = f"0{row_data}"

        return row_data


    def __dict_data(self) -> dict:
        return {
            "data":self.data,
            "hora_utc":self.hora_utc,
            "precipitao_total_horario_mm":self.precipitao_total_horario_mm,
            "pressao_atmosferica_ao_nivel_da_estacao_horaria_mb":self.pressao_atmosferica_ao_nivel_da_estacao_horaria_mb,
            "pressao_atmosferica_max_na_hora_ant_aut_mb":self.pressao_atmosferica_max_na_hora_ant_aut_mb,
            "pressao_atmosferica_min_na_hora_ant_aut_mb":self.pressao_atmosferica_min_na_hora_ant_aut_mb,
            "radiacao_global_kjm":self.radiacao_global_kjm,
            "temperatura_do_ar_bulbo_seco_horaria_c":self.temperatura_do_ar_bulbo_seco_horaria_c,
            "temperatura_do_ponto_de_orvalho_c":self.temperatura_do_ponto_de_orvalho_c,
            "temperatura_maxima_na_hora_ant_aut_c":self.temperatura_maxima_na_hora_ant_aut_c,
            "temperatura_minima_na_hora_ant_aut_c":self.temperatura_minima_na_hora_ant_aut_c,
            "temperatura_orvalho_max_na_hora_ant_aut_c":self.temperatura_orvalho_max_na_hora_ant_aut_c,
            "temperatura_orvalho_min_na_hora_ant_aut_c":self.temperatura_orvalho_min_na_hora_ant_aut_c,
            "umidade_rel_max_na_hora_ant_aut":self.umidade_rel_max_na_hora_ant_aut,
            "umidade_rel_min_na_hora_ant_aut":self.umidade_rel_min_na_hora_ant_aut,
            "umidade_relativa_do_ar_horaria":self.umidade_relativa_do_ar_horaria,
            "vento_direcao_horaria_gr":self.vento_direcao_horaria_gr,
            "vento_rajada_maxima_ms":self.vento_rajada_maxima_ms,
            "vento_velocidade_horaria_ms":self.vento_velocidade_horaria_ms,
        }
    
