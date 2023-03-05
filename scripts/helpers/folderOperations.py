import os

class CreateFolders:
    def __init__(self, array_directories:list) -> None:
        self.array_directories = array_directories

        self.__create()

    def __create(self) -> None:
        for directory in self.array_directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                