from typing import Optional
from ui.console_view import ConsoleView
from core.services import WebhookService


class WebhookCommand:
    def __init__(self, service: WebhookService, view: ConsoleView):
        self.service = service
        self.view = view

    def execute(self) -> None:
        while True:
            choice = self.view.ask_webhook_menu()

            if choice == "add":
                self._add_webhook()
            elif choice == "list":
                self._list_webhooks()
            elif choice == "delete":
                self._delete_webhook()
            elif choice == "back":
                return

    def _add_webhook(self) -> None:
        url = self.view.ask_webhook_url()
        if not url:
            return

        success = self.service.register_webhook(url)
        self.view.show_webhook_add_result(success)
        self.view.wait_for_enter()

    def _list_webhooks(self) -> None:
        webhooks = self.service.get_all_webhooks()
        self.view.show_webhook_list(webhooks)
        self.view.wait_for_enter()

    def _delete_webhook(self) -> None:
        webhooks = self.service.get_all_webhooks()
        if not webhooks:
            self.view.show_empty_webhook_list()
            self.view.wait_for_enter()
            return

        selected = self.view.ask_webhook_to_delete(webhooks)
        if not selected:
            return

        success = self.service.delete_webhook(selected.url)
        self.view.show_webhook_delete_result(success)
        self.view.wait_for_enter()