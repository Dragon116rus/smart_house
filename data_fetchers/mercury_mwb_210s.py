import logging
from playwright.sync_api import sync_playwright
import time

from data_fetchers.abstract_fetcher import AbstractFetcher


class Mwb210S(AbstractFetcher):
    def __init__(
        self, playwright_, ip="192.168.1.252", password="admin", data_table_name="test"
    ):
        self.data_table_name = data_table_name
        self._logger = logging.getLogger(__name__)
        self.base_url = f"http://{ip}/"
        self.password = password
        self.playwright = playwright_
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def login(self):
        try:
            self.page.goto(self.base_url)
            time.sleep(2)
        except Exception:
            self._logger.debug("[-] Router web not available")
            return False

        try:
            # Input password and submit
            pwd_input = self.page.query_selector("#adminPwd")
            if pwd_input:
                pwd_input.fill(self.password)

            submit_btn = self.page.query_selector("#loginBtn")
            if submit_btn:
                submit_btn.click()

            time.sleep(2)  # Wait for redirect

            self._logger.debug("[+] Logged in successfully")

        except Exception as e:
            self._logger.debug(
                "[!] Login may have already been done or login elements not found:", e
            )

        return True

    @staticmethod
    def parse_value(data: str):
        value = data.split()[0]
        value = value.replace("%", "")
        return float(value)

    def fetch_data(self):
        try:
            page_availability = self.login()

            if not page_availability:
                return {"Availability": int(page_availability)}


            ccq_elem = self.page.query_selector("#localDeviceCcqValue")
            ccq = ccq_elem.inner_text() if ccq_elem else "0"

            snr_elem = self.page.query_selector("#localDeviceSnrValue")
            snr = snr_elem.inner_text() if snr_elem else "0"

            signal_value_elem = self.page.query_selector("#localDeviceSignalValue")
            signal_value = signal_value_elem.inner_text() if signal_value_elem else "0"

            noise_value_elem = self.page.query_selector("#localDeviceNoiseValue")
            noise_value = noise_value_elem.inner_text() if noise_value_elem else "0"

            cpu_value_elem = self.page.query_selector("#localDeviceCpuValueApRight")
            cpu_value = noise_value_elem.inner_text() if cpu_value_elem else "0"

            return {
                "Availability": int(page_availability),
                "CCQ": self.parse_value(ccq),
                "SNR": self.parse_value(snr),
                "Signal value": self.parse_value(signal_value),
                "Noise value": self.parse_value(noise_value),
                "CPU loading": self.parse_value(cpu_value),
            }

        except Exception as e:
            print(f"[!] Error fetching data: {e}")
            return None

    def close(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    playwright_ = sync_playwright().start()
    parser = Mwb210S(playwright_=playwright_, password="admin")  # change password if needed
    data = parser.fetch_data()
    parser.close()

    if data:
        print("\nRouter Status:")
        for key, value in data.items():
            print(f"  {key}: {value}")
