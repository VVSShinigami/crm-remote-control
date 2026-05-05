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
    # GET_LIST = "get_list"
    # GET_BY_ID = "get_by_id"
    # GET_FIELDS = "get_fields"



@dataclass
class Webhook:
    url: str
    is_valid: bool = False
    pattern: str = r'^https://[a-zA-Z0-9-]+\.bitrix24\.[a-z]{2,}/rest/\d+/[a-zA-Z0-9]+/[a-zA-Z0-9]+/?$'


    def validate(self) -> bool:
        validate = re.fullmatch(pattern=self.pattern, string=self.url)
        if type(validate) == re.Match:
            self.is_valid = True
        return self.is_valid


@dataclass
class ReportFile:
    path: str
    created: bool = False


    def existing_path(self) -> bool:
        path = Path(self.path).exists()
        if path:
            self.created = True
        return self.created


@dataclass
class BatchRequest:
    webhook: Webhook
    method: MethodType
    entity: EntityType
    array: list[str]


    def __post_init__(self):
        if len(self.array) == 0:
            raise "Массив не содержит ни одного значения"
        return print("Валидный массив!")
    

    def api_request(self):
        pass