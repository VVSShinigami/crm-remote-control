from core.ports import WebhookHandler
from core.entities import Webhook

class WebhookStorage:
    def save(self, webhook: Webhook) -> None:
        try:
            with open("savedwebhooks.txt", "a", encoding='utf-8') as f:
                f.write(f"\n{webhook}")
        except:
            pass



    def get_all(self) -> list:
        try:
            with open("savedwebhooks.txt", "r", encoding='utf-8') as f:
                f.read()
        except:
            pass