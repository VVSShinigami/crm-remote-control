import json
from core.entities import Settings


class SettingsStorage:
    def load(self) -> dict:
        try:
            with open("settings.json", "r", encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return False
        

    def save(self, settings: Settings) -> None:
        try:
            data = {
                "pause_time": settings.pause_time,
                "report_enabled": settings.report_enabled,
                    "report_path": settings.report_path,
                "history_track": settings.history_track
        }
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False