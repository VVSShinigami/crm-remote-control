import requests # type: ignore
from typing import List, Optional


mock = list(range(2, 201, 2))


class RequestHandler:
    BATCH_SIZE = 50

    def __init__(self,
                 webhook: str,
                 id_array: Optional[List[int]] = None,
                 method: Optional[str] = None,
                 entity: Optional[str] = None,
                 pause_time: Optional[int] = None):
        self.webhook = webhook.rstrip('/')
        self.id_array = id_array or []
        self.method = method
        self.entity = entity
        self.pause_time = pause_time

    def _send_batch(self, ids: List[int]) -> dict:
        commands = {}
        for i, entity_id in enumerate(ids):
            commands[f"cmd_{i}"] = f"crm.{self.entity}.{self.method}?id={entity_id}"

        response = requests.post(
            url=f"{self.webhook}/batch",
            json={"cmd": commands, "halt": 0}
        )
        return response.json()

    def execute(self) -> None:
        if not self.id_array:
            print("Список ID пуст")
            return

        total = len(self.id_array)
        for start in range(0, total, self.BATCH_SIZE):
            chunk = self.id_array[start:start + self.BATCH_SIZE]
            batch_num = start // self.BATCH_SIZE + 1
            total_batches = (total + self.BATCH_SIZE - 1) // self.BATCH_SIZE

            print(f"Пакет {batch_num}/{total_batches} ({len(chunk)} шт.)")
            response = self._send_batch(chunk)
            print(f"Ответ: {response}")

            if self.pause_time and start + self.BATCH_SIZE < total:
                import time
                time.sleep(self.pause_time)