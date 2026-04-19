import requests
import os


class FileParser:
    '''
    Парсинг файлов различных типов - .xlsx, csv, txt
    '''
    files_type_dict = {
        ".xlsx": "PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00!\x00b\xee",
        ".csv": "1\r\n3\r\n5\r\n\r\n",
        ".text": ''
    }
    def __init__(self, file_path: str):
        self.file_path = file_path


    def _definition_file_type(self) -> str:
        try:
            with open(self.file_path, 'rb') as file:
                header = file.read(16)
                print(header)
        except (OSError, PermissionError):
            return None



if __name__ == "__main__":
    # test = FileParser('/home/godtears/Рабочий стол/Не существующие ID.xlsx')
    test = FileParser(r'C:\Users\alexa\OneDrive\Рабочий стол\сontacts.csv')
    test._definition_file_type()