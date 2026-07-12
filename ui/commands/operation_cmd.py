from typing import Optional
from ui.console_view import ConsoleView
from core.services import CrmOperationService


class OperationCommand:
    def __init__(self, service: CrmOperationService, view: ConsoleView):
        self.service = service
        self.view = view

    def execute(self) -> None:
        entity = self.view.ask_entity()
        if not entity:
            return

        method = self.view.ask_method()
        if not method:
            return

        file_path = self.view.ask_file_path()
        if not file_path:
            return

        result = self.service.execute_operation(
            entity=entity,
            method=method,
            file_path=file_path
        )

        self.view.show_operation_result(result)
        self.view.wait_for_enter()