import pandas as pd

class WorksheetOperations:
    def __init__(
            self, 
            worksheet_folder:str='', 
            worksheet_name:str='', 
            dataframe:pd.DataFrame=pd.DataFrame(), 
            dest_folder:str='', 
            format:str='', 
            sep:str=';', 
            sheet_name:int=0
        ) -> None:

        self.sep = sep
        self.format = format
        self.dataframe = dataframe
        self.sheet_name = sheet_name
        self.dest_folder = dest_folder
        self.worksheet_name = worksheet_name
        self.worksheet_folder = worksheet_folder


    def _open_worksheet(self) -> pd.DataFrame:
        if self.__is_valid_format():
            try:
                match self.format:
                    case 'csv':
                        df = pd.read_csv(f'{self.worksheet_folder}/{self.worksheet_name}.{self.format}', sep=self.sep)
                    
                    case 'xlsx':
                        df = pd.read_excel(f'{self.worksheet_folder}/{self.worksheet_name}.{self.format}', sheet_name=self.sheet_name)
            except:
                df = pd.DataFrame()

            return df

    
    def __is_valid_format(self, format_list:list=['xlsx', 'csv']) -> bool:
        if self.format in format_list:
            return True
        else:
            raise Exception('\nPlease, select a valid format of worksheet!!')


    def _save_worksheet(self) -> None:
        if self.__is_valid_format():
            match self.format:
                case 'csv':
                    self.dataframe.to_csv(f'{self.dest_folder}/{self.worksheet_name}.{self.format}', sep=self.sep, index=False)

                case 'xlsx':
                    self.dataframe.to_excel(f'{self.dest_folder}/{self.worksheet_name}.{self.format}', index=False)
