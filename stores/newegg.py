import requests
from html.parser import HTMLParser
from stores.interface.interface import StoreInterface


class NeweggParser(HTMLParser):
    out_of_stock = False

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if not self.out_of_stock and "out of stock" in data.lower():
            self.out_of_stock = True

    def feed(self, data):
        super().feed(data)
        return not self.out_of_stock


class Newegg(StoreInterface):

    def sku_to_url(self, sku: str) -> str:
        return "https://www.newegg.com/p/pl?d={}".format(sku)

    def is_in_stock(self, data: str) -> bool:
        return NeweggParser().feed(data)
