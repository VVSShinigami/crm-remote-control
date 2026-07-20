from typing import Optional
from ui.console_view import ConsoleView
from core.services import WebhookService
import functools

class WebhookCommand:
    def __init__(self, service: WebhookService, view: ConsoleView):
        self.service = service
        self.view = view


    @staticmethod
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
        while True:
            choice = self.view.ask_webhook_menu()
            if choice == "delete":
                self._delete_webhook()
            elif choice == "back":
                return choice


    @clear_dec
    def _add_webhook(self) -> None:
        url = self.view.ask_webhook_url()
        if not url:
            return None
        success = self.service.register_webhook(url)
        self.view.show_webhook_add_result(success)
        self.view.wait_for_enter()


    @clear_dec
    def _list_webhooks(self) -> None:
        webhooks = self.service.get_all_webhooks()
        self.view.wait_for_enter()


    @clear_dec
    def _delete_webhook(self) -> None:
        webhooks = self.service.get_all_webhooks()
        if not webhooks:
            self.view.show_empty_webhook_list()
            self.view.wait_for_enter()
            return None
        selected = self.view.ask_webhook_to_delete(webhooks)
        if not selected:
            return None
        success = self.service.delete_webhook(selected)
        self.view.show_webhook_delete_result(success)
        self.view.wait_for_enter()

