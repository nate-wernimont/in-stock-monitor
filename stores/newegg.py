from html.parser import HTMLParser
from stores.interface.interface import AbstractStore


class NeweggParser(HTMLParser):
    in_stock = False

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if not self.in_stock and "add to cart" in data.lower():
            self.in_stock = True

    def feed(self, data):
        super().feed(data)
        return self.in_stock


class Newegg(AbstractStore):

    def item_to_sku(self, item):
        # Newegg items are SKUs themselves
        return item

    def sku_to_url(self, sku: str) -> str:
        return "https://www.newegg.com/p/pl?d={}".format(sku)

    def is_in_stock(self, sku, data: str) -> bool:
        return NeweggParser().feed(data)
