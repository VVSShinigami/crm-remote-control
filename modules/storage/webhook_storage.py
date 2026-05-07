from core.ports import WebhookProtocol
from core.entities import Webhook


class WebhookStorage:
    def save(self, webhook: Webhook) -> None:
        try:
            with open("saved_webhooks.txt", "a", encoding='utf-8') as f:
                f.write(f"{webhook.url}\n")
        except OSError:
            pass


    def get_all(self) -> list[str]:
        try:
            with open("saved_webhooks.txt", "r", encoding='utf-8') as f:
                return list(f.read().split())
        except FileNotFoundError:
            pass


    def delete(self, webhook: Webhook) -> None:
        try:
            webhook_list = self.get_all()
            webhook_list = webhook_list.remove(webhook)
            with open("saved_webhooks.txt", "w", encoding='utf-8') as f:
                for x in webhook_list:
                    f.write(f"{x}\n")
        except FileNotFoundError:
            print("Файл не найден!!!!")
        except ValueError:
            print("Нет такого значения")