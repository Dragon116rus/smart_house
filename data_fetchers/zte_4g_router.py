import logging
from playwright.sync_api import sync_playwright
import time

from data_fetchers.abstract_fetcher import AbstractFetcher


class ZteMF79U(AbstractFetcher):
    def __init__(
        self, base_url="http://192.168.0.1", password="admin", data_table_name="test"
    ):
        self.data_table_name = data_table_name
        self._logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def login(self):
        try:
            self.page.goto(f"{self.base_url}/index.html")
            time.sleep(2)
        except Exception:
            self._logger.debug("[-] Router web not available")
            return False

        try:
            # Click login button to open modal, if needed
            login_btn = self.page.query_selector("#btnLogin")
            if login_btn:
                login_btn.click()
                time.sleep(1)

            # Input password and submit
            pwd_input = self.page.query_selector("#txtPwd")
            if pwd_input:
                pwd_input.fill(self.password)

            submit_btn = self.page.query_selector("#btnLogin")
            if submit_btn:
                submit_btn.click()

            time.sleep(2)  # Wait for redirect

            self._logger.debug("[+] Logged in successfully")

        except Exception as e:
            self._logger.debug(
                "[!] Login may have already been done or login elements not found:", e
            )

        return True

    def fetch_detailed_data(self):
        detailed_info_button = self.page.query_selector("#showDetailInfo")
        if detailed_info_button:
            detailed_info_button.click()

    @staticmethod
    def parse_antenna_value(data: str):
        value = data.split()[0]
        return float(value)

    def fetch_data(self):
        try:
            page_availability = self.login()

            if not page_availability:
                return {"Availability": int(page_availability)}

            self.page.goto(f"{self.base_url}/index.html#antenna")
            time.sleep(2)

            rssi_elem = self.page.query_selector("#m_rssi")
            network_type = rssi_elem.inner_text() if rssi_elem else "0"

            sinr_elem = self.page.query_selector("#m_sinr")
            sinr = sinr_elem.inner_text() if sinr_elem else "0"

            rsrp_elem = self.page.query_selector("#m_rsrp")
            rsrp = rsrp_elem.inner_text() if rsrp_elem else "0"

            rsrq_elem = self.page.query_selector("#m_rsrq")
            rsrq = rsrq_elem.inner_text() if rsrq_elem else "0"

            return {
                "Availability": int(page_availability),
                "RSSI": self.parse_antenna_value(network_type),
                "SINR": self.parse_antenna_value(sinr),
                "RSRP": self.parse_antenna_value(rsrp),
                "RSRQ": self.parse_antenna_value(rsrq),
            }

        except Exception as e:
            print(f"[!] Error fetching data: {e}")
            return None

    def close(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    parser = ZteMF79U(password="admin")  # change password if needed
    data = parser.fetch_data()
    parser.close()

    if data:
        print("\nRouter Status:")
        for key, value in data.items():
            print(f"  {key}: {value}")
