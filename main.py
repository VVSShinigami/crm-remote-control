from datetime import datetime
from pathlib import Path

from core.entities import Settings
from core.services import WebhookService, CrmOperationService, ReportService, SettingsService
from modules.storage.webhook_storage import WebhookStorage
from modules.storage.settings_storage import SettingsStorage
from modules.file_handlers.file_reader import FileParser
from ui.app import Application
from ui.console_view import ConsoleView


def main():
    webhook_storage = WebhookStorage()
    settings_storage = SettingsStorage()
    file_parser = FileParser()
    webhook_service = WebhookService(webhook_storage)
    settings_service = SettingsService(settings_storage)
    try:
        app_settings = settings_service.load_settings()
    except (FileNotFoundError, ValueError, TypeError):
        app_settings = Settings(
            pause_time=0.3,
            report_enabled=True,
            report_path=str(Path.home() / "Desktop"),
            history_track=True
        )
        settings_service.save_settings(app_settings)

    report_service = ReportService(settings=app_settings)
    
    op_service = CrmOperationService(
        file_parser=file_parser,
        report_service=report_service
    )

    view = ConsoleView()

    app = Application(
        webhook_service=webhook_service,
        op_service=op_service,
        settings_service=settings_service,
        view=view
    )

    app.run()


if __name__ == "__main__":
    main()