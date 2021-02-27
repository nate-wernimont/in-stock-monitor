from html.parser import HTMLParser
import requests
from stores.interface.interface import StoreInterface


class BestBuyParser(HTMLParser):
    inAddToCart = False
    addToCartText = ""

    def handle_starttag(self, tag, attrs):
        if tag == "button":
            for tuple in attrs:
                if tuple[0] == "class":
                    if "add-to-cart" in tuple[1]:
                        self.inAddToCart = True

    def handle_endtag(self, tag):
        self.inAddToCart = False

    def handle_data(self, data):
        if self.inAddToCart:
            self.addToCartText = data

    def feed(self, data):
        super().feed(data)
        return self.addToCartText


bestBuyHeaders = headers = {
    'authority': 'www.bestbuy.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}


class BestBuy(StoreInterface):

    def __init__(self):
        self.custom_headers = bestBuyHeaders

    def sku_to_url(self, sku: str) -> str:
        return 'https://www.bestbuy.com/site/searchpage.jsp?st={}'.format(sku)

    def is_in_stock(self, data: str) -> bool:
        addToCartText = BestBuyParser().feed(data)
        return addToCartText != "Sold Out"
