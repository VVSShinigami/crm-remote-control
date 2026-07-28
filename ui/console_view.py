from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.table import Table
import questionary
import functools
from ui.arts import shngm_art, welcome_message, action_notation, webhook_notation, bye_art
from core.entities import Settings


class ConsoleView:
    def __init__(self):
        self.console = Console(theme=Theme({"success": "green", "error": "red"}))
        self._style = questionary.Style([
            ('question', 'fg:#6D6875 bold'),
            ('pointer', 'fg:#E5989B bold'),
            ('highlighted', 'fg:#B5838D bold'),
            ('selected', 'fg:#FFB4A2'),
            ('instruction', 'fg:#8D99AE')
        ])

    def show_main_panel(self, mapping_type: Optional[str] = None) -> None:
        panel = Panel(
            Text(f"CRM remote control by {shngm_art}", justify="center", style="bold #d4a373"),
            subtitle="ver. 2.2",
            border_style="#217718",
            style="on #283618",
            expand=True,
            padding=(1, 5)
        )
        self.console.print(panel)
        if mapping_type == 'welcome':
            self.console.print(welcome_message)
        elif mapping_type == 'action_notation':
            self.console.print(action_notation)
        elif mapping_type == 'webhook_notation':
            self.console.print(webhook_notation)

    def clear(self) -> None:
        self.console.clear()


    @staticmethod
    def clear_dec(func) -> None:
        functools.wraps(func)
        def wrapper(*args, **kwargs):
            self_instance = args[0]
            self_instance.clear()
            self_instance.show_main_panel()
            res = func(*args, **kwargs)
            return res
        return wrapper


    def ask_main_menu(self) -> str:
        choices = ["Начать", "Инструкция", "Настройки", "Выйти"]
        return questionary.select(
            message='Главное меню:',
            choices=choices,
            style=self._style,
            qmark="⚙️"
        ).ask() or "exit"


    def ask_webhook_menu(self) -> str:
        choices = [
            "Удалить вебхук",
            "Назад"
        ]
        result = questionary.select(
            message='Управление вебхуками:',
            choices=choices,
            style=self._style,
            qmark="⚙️"
        ).ask()
        if result == "Удалить вебхук": 
            self.clear()
            self.show_main_panel()
            return "delete"
        return "back"


    def ask_start_webhook_menu(self) -> str | None:
        choices = [
            "Ввести вебхук",
            "Выбрать из сохраненных",
            "Назад"
        ]
        webhook = questionary.select(
            message='Управление вебхуками',
            choices=choices,
            style=self._style,
        ).ask()
        if webhook == "Назад":
            return None
        return webhook


    def choose_webhook(self, webhooks_list) -> str:
        webhook = questionary.select(
            message='Управление вебхуками',
            choices=webhooks_list,
            style=self._style
        ).ask()
        return webhook


    def ask_webhook_url(self) -> Optional[str]:
        self.console.print(webhook_notation)
        url = questionary.text(
            message="Введите URL вебхука:",
            style=self._style,
            qmark="🔗"
        ).ask()
        return url.strip() if url else None


    def show_webhook_add_result(self, success: bool) -> None:
        if success:
            self.console.print("[success]✅ Вебхук успешно сохранён![/success]")
        else:
            self.console.print("[error]❌ Ошибка: неверный формат или не удалось сохранить[/error]")


    def show_webhook_list(self, webhooks: list) -> str | None:
        choices = []
        if not webhooks:
            self.show_empty_webhook_list()
            return
        for idx, wh in enumerate(webhooks, 1):
            choices.append(wh)
            print(choices)
        choices.append("Назад")
        selected_webhook = questionary.select(
        message='Выберите нужный вебхук',
        choices=choices,
        style=self._style,
        qmark="🔗"
    ).ask()
        if selected_webhook == "Назад":
            return None
        else:
            return selected_webhook


    def show_empty_webhook_list(self) -> None:
        self.console.print("[yellow]Список вебхуков пуст[/yellow]")


    def ask_webhook_to_delete(self, webhooks: list):
        if not webhooks:
            return None
        
        choices = [getattr(wh, 'url', str(wh)) for wh in webhooks]
        choices.append("Назад")
        
        selected_url = questionary.select(
            message='Выберите вебхук для удаления:',
            choices=choices,
            style=self._style,
            qmark="🗑️"
        ).ask()

        if selected_url == "Назад":
            return None
            
        for wh in webhooks:
            if getattr(wh, 'url', str(wh)) == selected_url:
                return wh
        return None


    def show_webhook_delete_result(self, success: bool) -> None:
        if success:
            self.console.print("[success]Вебхук удалён![/success]")
        else:
            self.console.print("[error]Не удалось удалить вебхук[/error]")


    def wait_for_enter(self) -> None:
        questionary.press_any_key_to_continue(message="Нажмите любую клавишу для продолжения...").ask()


    def show_bye(self) -> None:
        self.console.print(bye_art)

    @clear_dec
    def ask_entity(self) -> Optional[str]:
        choices = ["Сделка", "Лид", "Контакт", "Компания", "Назад"]
        result = questionary.select(
            message="Выберите сущность:",
            choices=choices,
            style=self._style,
            qmark="📋"
        ).ask()
        return None if result == "Назад" else result


    def ask_method(self) -> Optional[str]:
        choices = ["Удалить", "Обновить", "Назад"]
        result = questionary.select(
            message="Выберите действие:",
            choices=choices,
            style=self._style,
            qmark="⚡"
        ).ask()
        return None if result == "Назад" else result

    @clear_dec
    def ask_file_path(self) -> Optional[str]:
        path = questionary.text(
            message="Путь к файлу с ID (xlsx/csv/txt):",
            style=self._style,
            qmark="📁"
        ).ask()
        return path.strip() if path else None


    def show_operation_result(self, result: dict) -> None:
        if not result.get("success"):
            self.console.print(f"[error]{result.get('message', 'Неизвестная ошибка')}[/error]")
            return

        processed = result.get("processed", 0)
        total = result.get("total", 0)
        report_path = result.get("report_path")

        self.console.print(f"[success]Выполнено: {processed}/{total}[/success]")
        if report_path:
            self.console.print(f"[success]📊 Отчет сохранен: {report_path}[/success]")


    # def show_current_settings(self, settings):
    #     print(settings)


    # def show_fail_settings(self):
    #     print(f"Настройки приложения не заданы!")

    def show_current_settings(self, settings: Settings) -> None:
        table = Table(title="Текущие настройки", border_style="#217718")
        table.add_column("Параметр", style="cyan")
        table.add_column("Значение", style="green", justify="right")

        table.add_row("Задержка между запросами", f"{settings.pause_time} сек")
        table.add_row("Генерация отчетов", "Да" if settings.report_enabled else "Нет")
        table.add_row("Отслеживание истории", "Да" if settings.history_track else "Нет")
        table.add_row("Путь для отчетов", settings.report_path)

        self.console.print(table)

    def ask_settings_action(self) -> str:
        choices = [
            "Изменить задержку",
            "Переключить отчеты",
            "Переключить историю",
            "Назад"
        ]
        result = questionary.select(
            message="Выберите настройку для изменения:",
            choices=choices,
            style=self._style
        ).ask()

        if result == "Изменить задержку": 
            return "pause_time"
        if result == "Переключить отчеты": 
            return "report_enabled"
        if result == "Переключить историю": 
            return "history_track"
        return "back"

    def ask_toggle_setting(self, current_value: bool, description: str) -> bool:
        result = questionary.confirm(
            message=f"{description} (сейчас {'вкл' if current_value else 'выкл'}). Переключить?",
            style=self._style,
            default=not current_value
        ).ask()
        
        return result if result is not None else current_value

    def ask_float_setting(self, current_value: float, description: str) -> float:
        result = questionary.text(
            message=f"{description} (сейчас {current_value}). Введите новое значение:",
            style=self._style
        ).ask()

        if not result:
            return current_value

        try:
            new_val = float(result)
            if new_val < 0:
                self.console.print("[error]Значение не может быть отрицательным[/error]")
                return current_value
            return new_val
        except ValueError:
            self.console.print("[error]Введите корректное число[/error]")
            return current_value


    def ask_toggle_setting(self, current_value: bool, description: str) -> bool:
        return questionary.confirm(
            message=f"{description} (сейчас {'вкл' if current_value else 'выкл'}). Переключить?",
            style=self._style,
            default=not current_value
        ).ask()

    def ask_float_setting(self, current_value: float, description: str) -> float:
        result = questionary.text(
            message=f"{description} (сейчас {current_value}). Введите новое значение:",
            style=self._style,
            validate=lambda val: True if self._is_valid_float(val) else "Введите число"
        ).ask()
        
        if result:
            try:
                return float(result)
            except ValueError:
                return current_value
        return current_value

    def _is_valid_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False