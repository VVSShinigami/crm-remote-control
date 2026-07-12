# # main.py
# from modules.storage.webhook_storage import WebhookStorage
# from core.entities import Webhook

# storage = WebhookStorage()

# webhook = Webhook(url="https://test.bitrix24.ru/rest/1/a/b/")

# print("Сохраняем...")
# storage.save(webhook)

# print("Загружаем:")
# all_webhooks = storage.get_all()
# for url in all_webhooks:
#     print(f"  - {url}")

# print("Удаляем...")
# storage.delete(webhook)

# print("Осталось:")
# remaining = storage.get_all()
# print(f"  Количество: {len(remaining)}")

from core.services import WebhookService
from modules.storage.webhook_storage import WebhookStorage
from ui.app import Application
from ui.console_view import ConsoleView


def main():
    storage = WebhookStorage()
    webhook_service = WebhookService(storage)
    view = ConsoleView()

    app = Application(
        webhook_service=webhook_service,
        op_service=None,
        view=view
    )

    app.run()


if __name__ == "__main__":
    main()