import csv
import pandas as pd

class GetDataFromCSV:
    def __init__(self, folder:str, filename:str) -> None:
        self.folder = folder
        self.filename = filename

        self.__get_data()


    def __get_data(self) -> pd.DataFrame:
        count = 0
        with open(f"{self.folder}/{self.filename}.csv", newline='', errors="ignore") as csvfile:
            data = csv.reader(csvfile, delimiter=';', quotechar=';')

            for row in data:
                if count < 20:

                    row_code_station = str(row[0])[0:6]
                    
                    if row_code_station == "CODIGO":
                        code_station = str(row[1])
                        print(code_station)

                count = count + 1



if __name__ == "__main__":
    folder = "/Users/yanpina/Downloads/2023"
    filename = "INMET_SE_SP_A771_SAO PAULO - INTERLAGOS_01-01-2023_A_31-01-2023"
    GetDataFromCSV(folder, filename)


# with open(path, 'r', encoding='utf-8', errors='ignore') as infile:
#      inputs = csv.reader(infile)

#      for index, row in enumerate(inputs):
#         print(row)
#         # Create file with no header
#         if index == 0:
#             continue
         
# import csv

# with open(path, 'r') as infile, open(path + 'final.csv', 'w') as outfile:

#     def unicode_csv(infile, outfile):
#         inputs = csv.reader(utf_8_encoder(infile))
#         output = csv.writer(outfile)

#         for index, row in enumerate(inputs):
#             yield [unicode(cell, 'utf-8') for cell in row]
#             if index == 0:
#                  continue
#         output.writerow(row)

#     def utf_8_encoder(infile):
#         for line in infile:
#             yield line.encode('utf-8')

# unicode_csv(infile, outfile)

# dataframe = WorksheetOperations(
#     worksheet_folder=folder, 
#     worksheet_name="INMET_SE_SP_A771_SAO PAULO - INTERLAGOS_01-01-2023_A_31-01-2023",
#     format="csv",
#     )._open_worksheet()

# print(dataframe)