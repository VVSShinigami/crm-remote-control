from ui.console_view import ConsoleView
from core.services import CrmOperationService, WebhookService
from modules.bitrix.client import BitrixClient
import functools


class SettingsCommand:
    def __init__(self, service):
        self.service = service


