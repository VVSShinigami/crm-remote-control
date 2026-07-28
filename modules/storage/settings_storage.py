import json


class SettingsStorage:
    def load(self) -> dict:
        try:
            with open("settings.json", "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return False