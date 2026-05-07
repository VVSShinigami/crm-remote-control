from core.entities import Webhook, ReportFile
from core.ports import WebhookProtocol, FileProtocol, BatchProtocol


class WebhookService:
    def __init__(self, storage: WebhookProtocol):
        self.storage = storage


    def check_webhook(self, url: str):
        webhook = Webhook(url=url)
        if not webhook.validate():
            return False
        else:
            self.storage.save(url)


    def get_all_webhooks(self) -> list[str]:
        return self.storage.load_all()


    def delete_webhook(self, url: str) -> None:
        webhook = Webhook(url=url)
        return self.storage.delete(webhook)
    

class ReportService:
    def __init__(self, storage: FileProtocol):
        self.storage = storage
    
    
    def create_report(self, path: str) -> bool:
        report = ReportFile(path=path)
        return self.storage.save(report)