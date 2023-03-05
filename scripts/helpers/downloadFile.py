import requests
from tqdm import tqdm


class DownloadFile:
    def __init__(
            self, 
            url:str, 
            format:str, 
            filename:str, 
            dest_folder:str, 
            download_message:str = "Downloading file..."
            ) -> None:
        
        self.url = url
        self.format = format
        self.filename = filename
        self.dest_folder = dest_folder
        self.download_message = download_message


        self.__create_session()
        self.__get()
        self.__download()


    def __download(self, chunk_size: int = 2048) -> None:
        response = self._session.get(self.url, stream=True, timeout=10)
    
        if not response.ok:
            raise Exception("Failed to get your file!")

        with open(f"{self.dest_folder}/{self.filename}.{self.format}", "wb") as fd:
            for chunk in tqdm(
                iterable=response.iter_content(chunk_size),
                total=int(response.headers.get("Content-Length", False) or 0) / chunk_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"{self.download_message}"
            ):
                fd.write(chunk)

        return True
    
    
    def __get(self):
        response = self._session.get(self.url, verify=False)
        assert response.ok, f"Oh no! Failed to access {self.url}"

        return response


    def __create_session(self) -> None:
        self._session = requests.Session()
