from ui.console_view import ConsoleView
from ui.commands.webhook_cmd import WebhookCommand
from ui.commands.operation_cmd import OperationCommand
from ui.commands.settings_cmd import SettingsCommand
from core.services import WebhookService, CrmOperationService, SettingsService


class Application:
    def __init__(
        self,
        webhook_service: WebhookService,
        op_service: CrmOperationService,
        settings_service: SettingsService,
        view: ConsoleView

    ):
        self.view = view
        self.webhook_cmd = WebhookCommand(webhook_service, view)
        self.op_cmd = OperationCommand(op_service, webhook_service, view)
        self.settings_op = SettingsCommand(settings_service, view)


    def run(self) -> None:
        while True:
            self.view.show_main_panel(mapping_type='welcome')
            choice = self.view.ask_main_menu()
            if choice == "Выйти":
                self.view.show_bye()
                break
            elif choice == "Начать":
                self.op_cmd.execute()
            elif choice == "Инструкция":
                self.view.console.print("Инструкция: https://github.com/VVSShinigami")
                self.view.wait_for_enter()
            elif choice == "Настройки":
                self.settings_op.execute()
                self.view.wait_for_enter()

            self.view.clear()