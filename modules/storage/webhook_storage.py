from core.ports import WebhookProtocol
from core.entities import Webhook
from pathlib import Path
import time

class WebhookStorage(WebhookProtocol):
    def __init__(self, path: str = "saved_webhooks.txt"):
        self.path = Path(path)


    def save(self, webhook: Webhook) -> bool:
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(f"{webhook.url}\n")
            return True
        except OSError:
            return False


    def load_all(self) -> list[str]:
        try:
            with open(self.path, "r", encoding='utf-8') as f:
                return list(f.read().split())
        except FileNotFoundError:
            pass


    def delete(self, webhook: Webhook) -> None:
        try:
            webhook_list = self.load_all()
            webhook_list = webhook_list.remove(webhook)
            with open(self.path, "w", encoding='utf-8') as f:
                for x in webhook_list:
                    f.write(f"{x}\n")
        except FileNotFoundError:
            print("Файл не найден")
        except ValueError:
            print("Нет такого значения")