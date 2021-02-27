class QueryException(Exception):
    pass


class StoreInterface:
    custom_headers = {}

    def sku_to_url(self, sku: str) -> str:
        """Convert a sku to a url to be loaded."""
        pass

    def is_in_stock(self, data: str) -> bool:
        """Returns whether the data found at a url indicates whether it is in stock."""
        pass
