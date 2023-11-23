import requests


class BoltMLClient(object):
    def __init__(self, api_endpoint, client_token):
        self.api_endpoint = api_endpoint
        self.client_token = client_token

    def log_event(
        self, session_id: str, event_type: str, event_name: str, event_data: dict = {}
    ):
        requests.post(
            self.api_endpoint + "/event?client_token=" + self.client_token,
            json={
                "session_id": session_id,
                "event_type": event_type,
                "event_name": event_name,
                "event_data": event_data,
            },
        )

    def apply_selector(self, session_id: str, selector_id: str, options: list):
        res = requests.post(
            self.api_endpoint
            + "/selector/"
            + selector_id
            + "?client_token="
            + self.client_token
            + "&session_id="
            + session_id,
            json=options,
        )
        return res.json()["value"]

    def fetch_or_create_objective(
        self,
        objective_name: str,
        positive: bool,
        event_type: str,
        event_name: str,
        time_window: int,
    ):
        res = requests.post(
            self.api_endpoint + "/objective?client_token=" + self.client_token,
            json={
                "objective_name": objective_name,
                "positive": positive,
                "event_type": event_type,
                "event_name": event_name,
                "time_window": time_window,
            },
        )
        return res.json()["objective_id"]

    def fetch_or_create_selector(
        self,
        selector_name: str,
        objective_id: str,
    ):
        res = requests.post(
            self.api_endpoint
            + "/selector?client_token="
            + self.client_token
            + "&objective_id="
            + objective_id
            + "&selector_name="
            + selector_name,
        )
        return res.json()["selector_id"]
