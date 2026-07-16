from typing import Optional
from ui.console_view import ConsoleView
from core.services import CrmOperationService, WebhookService
from modules.bitrix.client import BitrixClient


class OperationCommand:
    def __init__(self, service: CrmOperationService, webhook_service: WebhookService, view: ConsoleView):
        self.service = service
        self.view = view
        self.webhook_service = webhook_service

    def execute(self) -> None:
        webhook_url = self.view.ask_start_webhook_menu()
        if webhook_url is None:
            return
        elif webhook_url == "Выбрать из сохраненных":
            webhooks_list = self.webhook_service.get_all_webhooks()
            webhook_url = self.view.choose_webhook(webhooks_list)
        else:
            webhook_url = self.view.ask_webhook_url()
        entity = self.view.ask_entity()
        if not entity:
            return

        method = self.view.ask_method()
        if not method:
            return

        file_path = self.view.ask_file_path()
        if not file_path:
            return

        client = BitrixClient(webhook=webhook_url)

        result = self.service.execute_operation(
            bitrix_client=client,
            entity=entity,
            method=method,
            file_path=file_path
        )

        self.view.show_operation_result(result)
        self.view.wait_for_enter()