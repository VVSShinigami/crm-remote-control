from dataclasses import dataclass
from enum import Enum
import re
from pathlib import Path


class EntityType(Enum):
    DEAL = "deal"
    LEAD = "lead"
    CONTACT = "contact"
    COMPANY = "company"

class MethodType(Enum):
    DELETE = "delete"
    UPDATE = "update"
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"
    GET_FIELDS = "get_fields"



@dataclass
class Webhook:
    url: str
    is_valid: bool = False
    pattern: str = r'^https://[a-zA-Z0-9-]+\.bitrix24\.[a-z]{2,}/rest/\d+/[a-zA-Z0-9]+/[a-zA-Z0-9]+/?$'


    def validate(self):
        validate = re.fullmatch(pattern=self.pattern, string=self.url)
        if type(validate) == re.Match:
            self.is_valid = True
        return self.is_valid


@dataclass
class ReportFile:
    path: str
    created: bool = False


    def existing_path(self):
        path = Path(self.path).exists()
        if path:
            self.created = True
        return self.created



if __name__ == "__main__":
    # test1 = Webhook(url='https://loh.bitrix24.ru/rest/1/adfad/asdfdasf/')
    # test1 = Webhook(url='https://loh.bitrirest/1/adfadfadsf/asdfdasf')
    # print(test1._validate())

    test2 = ReportFile(path=r'C:\Users\alexa\OneDrive\Рабочий стол\crmka\asf')
    print(test2.existing_path())