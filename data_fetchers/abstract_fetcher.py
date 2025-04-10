class AbstractFetcher:
    def __init__(self, data_table_name="test"):
        self.data_table_name = data_table_name

    def fetch_data(self, *args, **kwargs) -> dict[str, float | int]:
        """
        Fetch data from the source.
        """
        raise NotImplementedError("Subclasses should implement this method.")
