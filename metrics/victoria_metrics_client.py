import json
import logging
import requests


class VictoriaMetricsClient:
    def __init__(self, db_url: str):
        self.endpoint = f"{db_url}/api/v1/import"
        self._logger = logging.getLogger(__name__)

    def push_data(
        self,
        metric_name: str,
        metric_values: list[float],
        timestamps: list[int],
        table_name: str = "test",
    ):
        data = [
            {
                "metric": {
                    "__name__": table_name,
                    "metric_name": metric_name,
                },
                "values": metric_values,
                "timestamps": timestamps,
            },
        ]
        jsonl_data = "\n".join([json.dumps(entry) for entry in data])
        response = requests.post(self.endpoint, data=jsonl_data)
        if response.status_code == 204:
            self._logger.debug(
                f"Data pushed successfully to {self.endpoint}: metric_name {metric_name}, metric_values {metric_values}"
            )
        else:
            self._logger.error(f"Error: {response.text}")
