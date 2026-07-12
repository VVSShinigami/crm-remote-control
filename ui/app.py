from ui.console_view import ConsoleView
from ui.commands.webhook_cmd import WebhookCommand
from ui.commands.operation_cmd import OperationCommand
from core.services import WebhookService, CrmOperationService


class Application:
    def __init__(
        self,
        webhook_service: WebhookService,
        op_service: CrmOperationService,
        view: ConsoleView
    ):
        self.view = view
        self.webhook_cmd = WebhookCommand(webhook_service, view)
        self.op_cmd = OperationCommand(op_service, view)

    def run(self) -> None:
        while True:
            self.view.show_main_panel(mapping_type='welcome')
            choice = self.view.ask_main_menu()

            if choice == "exit":
                self.view.show_bye()
                break
            elif choice == "webhooks":
                self.webhook_cmd.execute()
            elif choice == "start":
                self.op_cmd.execute()

            self.view.clear()