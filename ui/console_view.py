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
            "Список вебхуков",
            "Удалить вебхук",
            "Назад"
        ]
        result = questionary.select(
            message='Управление вебхуками:',
            choices=choices,
            style=self._style,
            qmark="⚙️"
        ).ask()
        if result == "Список вебхуков": 
            self.clear()
            self.show_main_panel()
            return "choosed"
        if result == "Удалить вебхук": 
            self.clear()
            self.show_main_panel()
            return "delete"
        return "back"

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

    def clear(self) -> None:
        self.console.clear()

    def show_bye(self) -> None:
        self.console.print(bye_art)

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