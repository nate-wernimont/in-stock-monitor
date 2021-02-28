import requests
import json
from html.parser import HTMLParser
from stores.interface.interface import AbstractStore
from stores.interface.interface import QueryException


class StaplesParser(HTMLParser):
    inStock = False

    def handle_starttag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        return

    def handle_data(self, data):
        if data == "Quantity":
            self.inStock = True

    def feed(self, data):
        super().feed(data)
        return self.inStock


class Staples(AbstractStore):

    def item_to_sku(self, items):
        # Staples items are SKUs themselves
        return items

    def sku_to_url(self, sku: str) -> str:
        response = requests.get(
            "https://www.staples.com/searchux/api/v1/{}/directory_{}".format(sku, sku))
        if response.status_code >= 400:
            print("Encountered bad status getting product info: {}".format(
                response.status_code))
            raise QueryException()

        return "https://staples.com{}".format(json.loads(response.content.decode("utf-8"))["path"])

    def is_in_stock(self, sku, data: str) -> bool:
        return StaplesParser().feed(data)
