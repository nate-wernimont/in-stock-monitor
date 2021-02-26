import requests
import json
import sys
from html.parser import HTMLParser
from stores.interface.interface import StoreInterface

class StaplesParser(HTMLParser):
    inStock = True

    def handle_starttag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        if data == "This item is out of stock":
            self.inStock = False

    def feed(self, data):
        super().feed(data)
        return self.inStock

class Staples(StoreInterface):

    def sku_to_url(self, sku: str) -> str:
        response = requests.get("https://www.staples.com/searchux/api/v1/{}/directory_{}".format(sku, sku))
        if response.status_code >= 400:
            print("Encountered bad status getting product info: {}".format(response.status_code))
            raise QueryException()
        
        return "https://staples.com{}".format(json.loads(response.content.decode("utf-8"))["path"])

    def is_in_stock(self, data: str) -> bool:
        return StaplesParser().feed(data)