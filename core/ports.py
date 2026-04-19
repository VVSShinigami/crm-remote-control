from core.model import Webhook
from typing import Protocol

class WebhookPort(Protocol):
    def status(self, webhook: Webhook):
        pass