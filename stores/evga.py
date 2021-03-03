from html.parser import HTMLParser
from stores.interface.interface import AbstractStore

evgaHeaders = headers = {
    'authority': 'www.evga.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}


class EVGAParser(HTMLParser):
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


class EVGA(AbstractStore):

    def __init__(self, config):
        super().__init__(config=config)
        self.custom_headers = evgaHeaders

    def item_to_sku(self, item):
        # EVGA items are SKUs themselves
        return item

    def sku_to_url(self, sku: str) -> str:
        return "https://www.evga.com/products/product.aspx?pn={}".format(sku)

    def is_in_stock(self, sku, data: str) -> bool:
        return EVGAParser().feed(data)
