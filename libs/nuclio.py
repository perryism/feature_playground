import requests, json


class nuclio:
    def __init__(self, port, host="0.0.0.0"):
        self.port = port
        self.host = f"http://{host}"

    def request(self, o):
        return requests.post(f"{self.host}:{self.port}", json=o)

class Ratio(nuclio):
    def __init__(self):
        self.client = nuclio(49341)
    
    def request(self, o, columns):
        if hasattr(o, "to_dict"):
            o = o.to_dict()

        body = {
            "data": o,
            "columns": columns
        }

        resp = self.client.request(body)
        #TODO: check status code
        resp_body = resp.content.decode()
        return float(resp_body)