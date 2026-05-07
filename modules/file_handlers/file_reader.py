import requests #type:ignore
import os
import magic


class FileParser:
    def __init__(self, file_path: str):
        self.file_path = file_path


    def _definition_file_type(self) -> str:
        try:
            file = magic.from_file(self.file_path, mime=True)
            print(f"Тип файла: {file}")
        except (OSError, PermissionError):
            return file



if __name__ == "__main__":
    # test = FileParser('/home/godtears/Рабочий стол/Не существующие ID.xlsx')
    test = FileParser(file_path=r'C:\Users\alexa\OneDrive\Рабочий стол\test.xlsx')
    test._definition_file_type()