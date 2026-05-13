import requests #type:ignore
import os
import mimetypes
import openpyxl
from openpyxl import load_workbook
import csv


class FileParser:
    def __init__(self, file_path: str):
        self.file_path = file_path


    def _file_exists(self) -> None:
        if os.path.isfile(self.file_path):
            return self._definition_file_type()
        raise FileExistsError            


    def _definition_file_type(self) -> str:
        try:
            file, _ = mimetypes.guess_type(self.file_path)
            print(f"Тип файла: {file}")
            return file
        except (OSError, PermissionError):
            pass


    def read_file(self) -> list[int]:
        result = []
        if self._file_exists():
            file_type = self._definition_file_type()
            print(file_type)
            if file_type == "text/plain":
                with open(self.file_path, "r", encoding='utf-8') as f:
                    for _ in f:
                        _ = _.strip()
                        if not _:
                            continue
                        try:
                            id = int(_)
                            result.append(id)
                        except ValueError:
                            print(f'Не число! - {_}')
                    return result
            elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                wb = load_workbook(self.file_path, read_only=True)
                sheet = wb.active
                for row in sheet.values:
                    for _ in row:
                        result.append(_)
                        print(result)
                return result
            elif file_type == "application/vnd.ms-excel":
                print('CSV')
                with open(self.file_path, "r", encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader: #!!!
                        print(row)
                        for r in row:
                            id = r[0].strip()
                            result.append(int(_))
                            print(result)
                return result



if __name__ == "__main__":
    # test = FileParser('/home/godtears/Рабочий стол/Не существующие ID.xlsx')
    test = FileParser(file_path=r'C:\Users\alexa\OneDrive\Рабочий стол\test2.csv')
    test = test.read_file()
    print(f"Джесткий тест: {test}")
