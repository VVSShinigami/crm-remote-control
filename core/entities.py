from dataclasses import dataclass
from enum import Enum
import re
from pathlib import Path
from typing import List
import json


class EntityType(Enum):
    DEAL = "deal"
    LEAD = "lead"
    CONTACT = "contact"
    COMPANY = "company"


class MethodType(Enum):
    DELETE = "delete"
    UPDATE = "update"


@dataclass
class Webhook:
    url: str
    is_valid: bool = False
    pattern: str = r'^https://[a-zA-Z0-9-]+\.bitrix24\.[a-z]{2,}/rest/\d+/[a-zA-Z0-9]+(?:/[a-zA-Z0-9]+)?/?$'


    def validate(self) -> bool:
        match = re.fullmatch(pattern=self.pattern, string=self.url)
        return match is not None


@dataclass
class ReportFile:
    path: str
    created: bool = False


    def existing_path(self) -> bool:
        exists = Path(self.path).exists()
        if exists:
            self.created = True
        return exists


@dataclass
class BatchCommand:
    entity: EntityType
    method: MethodType
    ids: List[int]


    def __post_init__(self):
        if not self.ids:
            raise ValueError("BatchCommand не может быть создан с пустым списком ID")


    def to_api_payload(self) -> dict:
        commands = {
            f"cmd_{i}": f"crm.{self.entity.value}.{self.method.value}?id={entity_id}"
            for i, entity_id in enumerate(self.ids)
        }
        return {"cmd": commands, "halt": 0}
    

@dataclass
class Settings:
    pause_time: float
    report_enabled: bool
    report_path: str
    history_track: bool


    def validate(self) -> bool:
        if not isinstance(self.pause_time, (int, float)) or self.pause_time < 0:
            return False
        if not isinstance(self.report_enabled, bool):
            return False
        if not isinstance(self.report_path, str) or not self.report_path.strip():
            return False
        if not isinstance(self.history_track, bool):
            return False
        return True