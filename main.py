from datetime import datetime
from pathlib import Path

from core.services import WebhookService, CrmOperationService, ReportService
from modules.storage.webhook_storage import WebhookStorage
from modules.file_handlers.file_reader import FileParser
from modules.bitrix.client import BitrixClient
from ui.app import Application
from ui.console_view import ConsoleView


def main():
    storage = WebhookStorage()
    file_parser = FileParser()

    webhook_service = WebhookService(storage)

    settings = {
        "report_enabled": True,
        "pause_time": 0.3
    }

    report_service = ReportService(settings=settings)
    view = ConsoleView()

    op_service = CrmOperationService(
        file_parser=file_parser,
        report_service=report_service
    )

    app = Application(
        webhook_service=webhook_service,
        op_service=op_service,
        view=view
    )

    app.run()


if __name__ == "__main__":
    main()