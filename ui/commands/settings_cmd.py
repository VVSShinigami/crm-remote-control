from ui.console_view import ConsoleView
from core.services import SettingsService
import functools


class SettingsCommand:
    def __init__(self, service: SettingsService, view: ConsoleView):
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


    def execute(self) -> None:
        while True:
            self.view.show_current_settings(self.service.load_settings())
            choice = self.view.ask_settings_action()

            if choice == "back":
                self.settings_service.save_settings(self.settings)
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

    # @clear_dec
    # def input_settings(self):
    #     settings = self.service.load_settings()
    #     if settings == None:
    #         self.view.show_fail_settings()
    #         return
    #     self.view.show_current_settings(settings=settings)



