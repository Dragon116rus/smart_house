import logging
import time
import os
import yaml

from data_fetchers import DATA_FETCHERS
from data_fetchers.abstract_fetcher import AbstractFetcher
from metrics import DATABASES
from metrics.victoria_metrics_client import VictoriaMetricsClient
from utils.helpers import get_current_timestamp


def main():
    logger = logging.getLogger(__name__)
    # Load configuration from the YAML file
    config_path = os.getenv("CONFIG_PATH", "./config/config.yaml")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    logger.setLevel(config.get("LogLevel", "DEBUG"))
    logging.basicConfig(
        level=logger.level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info(f"Configuration loaded from {config_path}")
    logger.info(f"Log level set to {logger.level}")

    # Initialize the fetchers and database clients from the config
    fetchers: list[AbstractFetcher] = []
    for fetcher_config in config.get("Fetchers", []):
        fetcher_type = fetcher_config["type"]
        fetcher_params = fetcher_config.get("params", {})
        if fetcher_type in DATA_FETCHERS:
            fetchers.append(DATA_FETCHERS[fetcher_type](**fetcher_params))
        else:
            logger.warning(f"[!] Unknown fetcher type: {fetcher_type}")

    databases: list[VictoriaMetricsClient] = []
    for db_config in config.get("Databases", []):
        db_type = db_config["type"]
        db_params = db_config.get("params", {})
        if db_type in DATABASES:
            databases.append(DATABASES[db_type](**db_params))
        else:
            logger.warning(f"[!] Unknown database type: {db_type}")

    if not fetchers or not databases:
        logger.warning("[!] No valid fetchers or databases configured. Exiting.")
        return

    fetching_interval = config.get("FetchingInterval", 300)

    # Main loop
    while True:
        for fetcher in fetchers:
            # Fetch data from each fetcher
            data = fetcher.fetch_data()

            # Push data to each database
            for db_client in databases:
                for metric_name, metric_value in data.items():
                    db_client.push_data(
                        metric_name=metric_name,
                        metric_values=[metric_value],
                        timestamps=[get_current_timestamp()],
                        table_name=fetcher.data_table_name,
                    )

        time.sleep(fetching_interval)


if __name__ == "__main__":
    main()
