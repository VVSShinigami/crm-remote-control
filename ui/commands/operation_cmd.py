from typing import Optional
from ui.console_view import ConsoleView
from core.services import CrmOperationService, WebhookService
from modules.bitrix.client import BitrixClient
import functools



class OperationCommand:
    def __init__(self, service: CrmOperationService, webhook_service: WebhookService, view: ConsoleView):
        self.service = service
        self.view = view
        self.webhook_service = webhook_service


    def clear_dec(func) -> None:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self_instance = args[0]
            self_instance.view.clear()
            self_instance.view.show_main_panel()
            res = func(*args, **kwargs)
            return res
        return wrapper

    @clear_dec
    def execute(self) -> None:
        webhook_url = self.view.ask_start_webhook_menu()
        if webhook_url is None:
            return None
        elif webhook_url == "Выбрать из сохраненных":
            webhooks_list = self.webhook_service.get_all_webhooks()
            webhook_url = self.view.choose_webhook(webhooks_list)
        else:
            while True:
                url = self.view.ask_webhook_url()
                webhook_entity = self.webhook_service.register_webhook(url=url)
                if webhook_entity != True:
                    self.view.console.print("[error]Ошибка: Неверный формат вебхука[/error]")
                else:
                    self.view.console.print("[success]Вебхук принят[/success]")
                    break
        entity = self.view.ask_entity()
        if not entity:
            return None
        method = self.view.ask_method()
        if not method:
            return None
        file_path = self.view.ask_file_path()
        if not file_path:
            return None
        client = BitrixClient(webhook=url)
        result = self.service.execute_operation(
            bitrix_client=client,
            entity=entity,
            method=method,
            file_path=file_path
        )
        self.view.show_operation_result(result)
        self.view.wait_for_enter()