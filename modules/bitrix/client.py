import requests
from typing import List, Dict, Tuple
from rich.progress import track
import time
from urllib.parse import quote


class BitrixClient:
    BATCH_SIZE = 50

    def __init__(self, webhook: str, pause_time: float = 0.3):
        self.webhook = webhook.rstrip('/')
        self.pause_time = pause_time

    def execute_batch(
        self,
        ids: List[int],
        entity: str,
        method: str,
        field_id: str | None,
        field_value: str | None
    ) -> Tuple[List[int], List[int]]:
        realized_ids: List[int] = []
        unrealized_ids: List[int] = []
        total = len(ids)

        for start in track(range(0, total, self.BATCH_SIZE), description="Выполняется..."):
            chunk = ids[start:start + self.BATCH_SIZE]
            commands = {}
            cmd_to_id_map: Dict[str, int] = {}

            for i, entity_id in enumerate(chunk):
                cmd_key = f"cmd_{i}"
                if field_id is None:
                    commands[cmd_key] = f"crm.{entity}.{method}?id={entity_id}"
                else:
                    commands[cmd_key] = f"crm.{entity}.{method}?id={entity_id}&fields[{field_id}]={field_value}"
                cmd_to_id_map[cmd_key] = entity_id

            response = requests.post(
                url=f"{self.webhook}/batch",
                json={"cmd": commands, "halt": 0}
            ).json()
            batch_result = response.get("result", {})
            result_data = batch_result.get("result", {})
            result_errors = batch_result.get("result_error", {})

            for cmd_key, original_id in cmd_to_id_map.items():
                if cmd_key in result_errors:
                    unrealized_ids.append(original_id)
                elif cmd_key in result_data:
                    realized_ids.append(original_id)
                else:
                    unrealized_ids.append(original_id)

            if self.pause_time and start + self.BATCH_SIZE < total:
                time.sleep(self.pause_time)

        return realized_ids, unrealized_ids