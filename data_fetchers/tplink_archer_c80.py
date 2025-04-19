import logging
import os
from playwright.sync_api import sync_playwright

from data_fetchers.abstract_fetcher import AbstractFetcher


class TplinkArcherC80(AbstractFetcher):
    def __init__(self, playwright_, ip="192.168.0.1", password="admin", data_table_name="test"):
        self._logger = logging.getLogger(__name__)
        self.data_table_name = data_table_name
        self._logger = logging.getLogger(__name__)
        self.base_url = f"http://{ip}/"
        self.password = password

        self.playwright = playwright_
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def login(self):
        try:
            self.page.goto(self.base_url, timeout=3000)
        except Exception:
            self._logger.debug("[-] Router web not aviable")
            return False

        # Check is login required
        self.page.wait_for_timeout(2000)
        current_url = self.page.url
        if current_url == f"{self.base_url}#networkMap":
            self._logger.debug("[+] Already logged in")
            return True

        try:
            # Input password and submit
            password_field = self.page.locator("#local-pwd-tb")
            if password_field is None:
                raise Exception("Password field not found")
            input_field = password_field.locator("input, textarea").first
            if input_field:
                input_field.fill(self.password)

            submit_btn = self.page.locator("#local-login-button")
            if submit_btn:
                submit_btn.click()

            self.page.wait_for_timeout(2000)  # Wait for redirect
            current_url = self.page.url

            if current_url == f"{self.base_url}#networkMap":
                self._logger.debug("[+] Logged in successfully")
            else:
                self._logger.debug("[!] Login failed or page not redirected correctly")

        except Exception as e:
            self._logger.debug(
                "[!] Login may have already been done or login elements not found:", e
            )

        return True

    def fetch_data(self):
        try:
            page_aviability = self.login()

            if not page_aviability:
                return {"Aviability": int(page_aviability)}

            self.page.goto(f"{self.base_url}#networkMap")
            self.page.wait_for_timeout(2000)

            clients_field = self.page.locator("#map-clients")
            num_clients = clients_field.locator(".map-clients-icon-num").inner_text()

            return {
                "Aviability": int(page_aviability),
                "num_clients": int(num_clients),
            }

        except Exception as e:
            print(f"[!] Error fetching data: {e}")
            return None


if __name__ == "__main__":
    password = os.getenv("ROUTER_PASSWORD", "admin")
    url = os.getenv("ROUTER_URL", "http://192.168.0.1")
    playwright_ = sync_playwright().start()
    parser = TplinkArcherC80(playwright_=playwright_, password=password, ip=url)  # change password if needed
    data = parser.fetch_data()

    if data:
        print("\nRouter data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
