from core.services import WebhookService
from modules.storage.webhook_storage import WebhookStorage

def main():
    storage = WebhookStorage()
    service = WebhookService(storage=storage)
    result = service.check_webhook('https://sdf.bitrix24.ru/rest/1/asfasfdadfasdf/')


if __name__ == "__main__":
    main()