from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
import questionary
from ui.arts import shngm_art, welcome_message, action_notation, webhook_notation, bye_art


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

    def ask_main_menu(self) -> str:
        choices = ["Начать", "Вебхуки", "Инструкция", "Настройки", "Выйти"]
        return questionary.select(
            message='Главное меню:',
            choices=choices,
            style=self._style,
            qmark="⚙️"
        ).ask() or "exit"

    def ask_webhook_menu(self) -> str:
        choices = [
            ("Добавить вебхук", "add"),
            ("Список вебхуков", "list"),
            ("Удалить вебхук", "delete"),
            ("Назад", "back")
        ]
        return questionary.select(
            message='Управление вебхуками:',
            choices=choices,
            style=self._style,
            qmark="⚙️"
        ).ask() or "back"

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
            self.console.print("Вебхук успешно сохранён!")
        else:
            self.console.print("Ошибка: неверный формат или не удалось сохранить")

    def show_webhook_list(self, webhooks: list) -> None:
        if not webhooks:
            self.show_empty_webhook_list()
            return
        for idx, wh in enumerate(webhooks, 1):
            status = "ok" if getattr(wh, 'is_valid', True) else "bad"
            url = getattr(wh, 'url', str(wh))
            self.console.print(f"  {idx}. {status} {url}")

    def show_empty_webhook_list(self) -> None:
        self.console.print("Список вебхуков пуст")

    def ask_webhook_to_delete(self, webhooks: list):
        choices = [(getattr(wh, 'url', str(wh)), wh) for wh in webhooks]
        choices.append(("Назад", None))
        selected = questionary.select(
            message='Выберите вебхук для удаления:',
            choices=choices,
            style=self._style,
            qmark="🗑️"
        ).ask()
        return selected

    def show_webhook_delete_result(self, success: bool) -> None:
        if success:
            self.console.print("Вебхук удалён!")
        else:
            self.console.print("Не удалось удалить вебхук")

    def wait_for_enter(self) -> None:
        questionary.press_any_key_to_continue(message="Нажмите любую клавишу для продолжения...").ask()

    def clear(self) -> None:
        self.console.clear()

    def show_bye(self) -> None:
        self.console.print(bye_art)