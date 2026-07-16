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
        self.op_cmd = OperationCommand(op_service, webhook_service, view)

    def run(self) -> None:
        while True:
            self.view.show_main_panel(mapping_type='welcome')
            choice = self.view.ask_main_menu()

            if choice == "Выйти":
                self.view.show_bye()
                break
            elif choice == "Вебхуки":
                self.webhook_cmd.execute()
            elif choice == "Начать":
                self.op_cmd.execute()
            elif choice == "Инструкция":
                self.view.console.print("Инструкция: https://github.com/VVSShinigami")
                self.view.wait_for_enter()
            elif choice == "Настройки":
                self.view.console.print("Обновите версию приложения, в данной версии настройки не доступны")
                self.view.wait_for_enter()

            self.view.clear()