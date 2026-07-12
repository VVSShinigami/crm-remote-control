from typing import List
from core.entities import Webhook, ReportFile, BatchCommand, EntityType, MethodType
from core.ports import WebhookProtocol, FileProtocol, BatchProtocol


class WebhookService:
    def __init__(self, storage: WebhookProtocol):
        self.storage = storage

    def register_webhook(self, url: str) -> bool:
        webhook = Webhook(url=url)
        if not webhook.validate():
            return False
        return self.storage.save(webhook)

    def get_all_webhooks(self) -> list:
        return self.storage.load_all()

    def delete_webhook(self, url: str) -> bool:
        webhook = Webhook(url=url)
        return self.storage.delete(webhook)


class ReportService:
    def __init__(self, storage: FileProtocol):
        self.storage = storage

    def create_report(self, path: str) -> bool:
        report = ReportFile(path=path)
        return self.storage.save(report)


class CrmOperationService:
    def __init__(self, bitrix_client: BatchProtocol, file_parser: FileProtocol):
        self.bitrix_client = bitrix_client
        self.file_parser = file_parser

    def execute_operation(self, entity: str, method: str, file_path: str) -> dict:
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

        results = self.bitrix_client.execute_batch(
            ids=ids,
            entity=entity_type.value,
            method=method_type.value
        )

        processed = sum(len(r.get("result", {})) for r in results)
        total = len(ids)

        return {
            "success": True,
            "processed": processed,
            "total": total,
            "results": results
        }