import logging
import requests

from data_fetchers.abstract_fetcher import AbstractFetcher


class PageAviabilityChecker(AbstractFetcher):
    def __init__(self, url, data_table_name="test"):
        self.url = url
        self.data_table_name = data_table_name
        self._logger = logging.getLogger(__name__)

    def check_availability(self):
        try:
            response = requests.get(self.url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def fetch_data(self):
        """
        Fetch data from the router.
        """
        is_available = self.check_availability()
        return {"is_available": int(is_available)}
