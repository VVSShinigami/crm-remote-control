from ui.console_view import ConsoleView
from core.services import SettingsService
import functools


class SettingsCommand:
    def __init__(self, service: SettingsService, view: ConsoleView):
        self.service = service
        self.view = view
        self.settings = self.service.load_settings()

    
    def execute(self) -> None:
        while True:
            self.view.clear()
            self.view.show_main_panel()
            self.view.show_current_settings(self.settings)
            choice = self.view.ask_settings_action()

            if choice == "back":
                self.service.save_settings(self.settings)
                return
            elif choice == "pause_time":
                self.settings.pause_time = self.view.ask_float_setting(
                    self.settings.pause_time, 
                    "Задержка между запросами (сек)"
                )
            elif choice == "report_enabled":
                self.settings.report_enabled = self.view.ask_toggle_setting(
                    self.settings.report_enabled, 
                    "Генерация Excel-отчетов"
                )
            elif choice == "history_track":
                self.settings.history_track = self.view.ask_toggle_setting(
                    self.settings.history_track, 
                    "Отслеживание истории операций"
                )