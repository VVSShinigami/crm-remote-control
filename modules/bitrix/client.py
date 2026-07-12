import requests
from typing import List, Optional
import time

class BitrixClient:
    BATCH_SIZE = 50

    def __init__(self, webhook: str, pause_time: float = 0.3):
        self.webhook = webhook.rstrip('/')
        self.pause_time = pause_time

    def execute_batch(
        self,
        ids: List[int],
        entity: str,
        method: str
    ) -> List[dict]:
        results = []
        total = len(ids)

        for start in range(0, total, self.BATCH_SIZE):
            chunk = ids[start:start + self.BATCH_SIZE]
            commands = {}

            for i, entity_id in enumerate(chunk):
                commands[f"cmd_{i}"] = f"crm.{entity}.{method}?id={entity_id}"

            response = requests.post(
                url=f"{self.webhook}/batch",
                json={"cmd": commands, "halt": 0}
            )
            results.append(response.json())

            if self.pause_time and start + self.BATCH_SIZE < total:
                time.sleep(self.pause_time)

        return results