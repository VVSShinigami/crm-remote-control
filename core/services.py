from typing import List
from core.entities import Webhook, ReportFile, BatchCommand, EntityType, MethodType, Settings
from core.ports import WebhookProtocol, FileProtocol, BatchProtocol, SettingsStorageProtocol
from datetime import datetime
from pathlib import Path
from typing import Optional
from modules.excelreport.report import ExcelReport


class WebhookService:
    def __init__(self, storage: WebhookProtocol):
        self.storage = storage

    def register_webhook(self, url: str) -> bool:
        webhook = Webhook(url=url)
        return webhook.validate()

    def save_webhook(self, url: str) -> bool:
        webhook = Webhook(url=url)
        if not webhook.validate():
            return False
        return self.storage.save(webhook)

    def get_all_webhooks(self) -> list:
        return self.storage.load_all()

    def delete_webhook(self, url: str) -> bool:
        webhook = Webhook(url=url)
        return self.storage.delete(webhook)


class CrmOperationService:
    def __init__(self, file_parser, report_service):
        self.file_parser = file_parser
        self.report_service = report_service

    def execute_operation(
        self,
        bitrix_client,
        entity: str,
        method: str,
        file_path: str,
        field_id: str = None,
        field_value: str = None
    ) -> dict:
        ids = self.file_parser.read_file(file_path)
        if not ids:
            return {"success": False, "message": "Файл пуст или не найден"}

        entity_map = {
            "Сделка": EntityType.DEAL,
            "Лид": EntityType.LEAD,
            "Контакт": EntityType.CONTACT,
            "Компания": EntityType.COMPANY
        }

        method_map = {
            "Удалить": MethodType.DELETE,
            "Обновить": MethodType.UPDATE
        }

        entity_type = entity_map.get(entity)
        method_type = method_map.get(method)

        if not entity_type or not method_type:
            return {"success": False, "message": f"Неизвестная операция: {entity} / {method}"}
        realized_ids, unrealized_ids = bitrix_client.execute_batch(
            ids=ids,
            entity=entity_type.value,
            method=method_type.value,
            field_id=field_id,
            field_value=field_value
        )

        total = len(ids)
        processed = len(realized_ids)
        report_path = None
        if self.report_service:
            report_path = self.report_service.create_report(
                realized=realized_ids,
                unrealized=unrealized_ids
            )

        return {
            "success": True,
            "processed": processed,
            "total": total,
            "realized": realized_ids,
            "unrealized": unrealized_ids,
            "report_path": report_path
        }


class ReportService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_report(self, realized: list[int], unrealized: list[int]) -> str | None:
        if not getattr(self.settings, "report_enabled", True):
            return None

        filename = f"Отчет_{datetime.now().strftime('%d.%m.%Y_%H_%M_%S')}.xlsx"
        output_path = str(Path(self.settings.report_path) / filename)

        report = ExcelReport(realized_ids=realized, unrealized_ids=unrealized)
        if report.generate(output_path):
            return output_path
        return None


class SettingsService:
    def __init__(self, storage: SettingsStorageProtocol):
        self.storage = storage

    def load_settings(self) -> Settings:
        data = self.storage.load()
        if data is False:
            raise FileNotFoundError("settings.json не найден")
        settings = Settings(**data)
        if not settings.validate():
            raise ValueError("Некорректные настройки")
        return settings

    def save_settings(self, settings: Settings) -> bool:
        return self.storage.save(settings)