class QueryException(Exception):
    pass


class AbstractStore:
    custom_headers = {}

    def __init__(self, config):
        self.config = config

    def item_to_sku(self, items):
        """Converts ini formatted item to sku."""
        pass

    def sku_to_url(self, sku: str) -> str:
        """Convert a sku to a url to be loaded."""
        pass

    def is_in_stock(self, sku: str, data: str) -> bool:
        """Returns whether the webpage found for the sku indicates whether it is in stock."""
        pass


class AbstractBuyableStore(AbstractStore):

    def __init__(self, config):
        super().__init__(config)

    def buy_item(self, sku):
        pass
