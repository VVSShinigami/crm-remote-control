import requests

mock = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200]
class RequestHandler:
    def __init__(self, 
                 webhook: str, 
                 pause_time=None | int, 
                 id_array=None | list, 
                 method=None | str,
                 entity=None | str):
        self.webhook = webhook
        self.pause_time = pause_time
        self.id_array = id_array
        self.method = method
        self.entity = entity


    def _batch(self) -> str:
        commands = {}
        counter = 0
        while counter < 50:
            for num, entity_id in enumerate(self.id_array):
                commands[f"uniqe_{num}"] = f"crm.{self.entity}.{self.method}?id={entity_id}"


        response = requests.post(url=f"{self.webhook}/batch", json={
            "cmd": commands,
            "halt": 0,
        }).json()

        print(f"Отработка : {response}")


if __name__ == "__main__":
    test = RequestHandler(webhook='https://b24-3w6bzp.bitrix24.ru/rest/1/7h6p7a3cvtehfvgw/', id_array=mock, method='delete', entity='deal')
    test._batch()