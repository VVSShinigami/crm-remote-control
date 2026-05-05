from core.entities import Webhook
from core.ports import WebhookProtocol



class WebhookService:
    def __init__(self, storage: WebhookProtocol):
        self.storage = storage


    def check_webhook(self, url: str):
        webhook = Webhook(url=url)
        if not webhook.validate():
            return False
        else:
            self.storage.save(url)


    def save_webhook(self):
        return self.storage.load_all()
    

    def print_notification(self):
        ...