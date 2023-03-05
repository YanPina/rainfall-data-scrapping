import os
from glob import glob
from time import sleep
from pathlib import Path


class CheckFileDownload:
    def __init__(self, filename:str, file_folder:str, file_format:str, print_confirmation:bool=True) -> None:
        self.filename = filename
        self.file_format = file_format
        self.file_folder = file_folder
        self.print_confirmation = print_confirmation
        

    def _check_download_finished(
        self, 
        file_in_folder:bool=False, 
        try_limit:int=0,
        max_try:int=15, #seconds
        latest_file_in_download_folder:str=''
    ):
        while (file_in_folder == False) & (try_limit < max_try):
            sleep(1)
            latest_file_in_download_folder = self.__latest_file_in_folder()
            
            if latest_file_in_download_folder.endswith(self.file_format):
                if Path(latest_file_in_download_folder).stem == self.filename:
                    if self.print_confirmation:
                        print(f'"{self.filename}" downloaded!!')
                    file_in_folder = True
            try_limit += 1


    def __latest_file_in_folder(self):
        list_of_files = glob(f'{self.file_folder}\\*')

        return max(list_of_files, key=os.path.getctime)
    