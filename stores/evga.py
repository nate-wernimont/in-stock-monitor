import requests
from html.parser import HTMLParser
from stores.interface.interface import StoreInterface

evgaHeaders = headers = {
    'authority': 'www.evga.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}


class EVGAParser(HTMLParser):
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


class EVGA(StoreInterface):

    def __init__(self):
        self.custom_headers = evgaHeaders

    def sku_to_url(self, sku: str) -> str:
        return "https://www.evga.com/products/product.aspx?pn={}".format(sku)

    def is_in_stock(self, data: str) -> bool:
        return EVGAParser().feed(data)
