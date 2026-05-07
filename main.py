# main.py
from modules.storage.webhook_storage import WebhookStorage
from core.entities import Webhook

# 1. Создаем адаптер
storage = WebhookStorage()

# 2. Создаем вебхук
webhook = Webhook(url="https://test.bitrix24.ru/rest/1/a/b/")

# 3. Сохраняем
print("Сохраняем...")
storage.save(webhook)

# 4. Загружаем
print("Загружаем:")
all_webhooks = storage.get_all()
for url in all_webhooks:
    print(f"  - {url}")

# 5. Удаляем
print("Удаляем...")
storage.delete(webhook)

# 6. Проверяем
print("Осталось:")
remaining = storage.get_all()
print(f"  Количество: {len(remaining)}")