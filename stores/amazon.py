from html.parser import HTMLParser
from stores.interface.interface import AbstractStore
from enum import Enum
from selenium import webdriver

amazonHeaders = headers = {
    'authority': 'www.amazon.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}


class AmazonParser(HTMLParser):
    in_stock = False
    price = -1.0
    next_data_price = False

    def handle_starttag(self, tag, attrs):
        if not self.in_stock and tag == "input":
            for attrName, attrValue in attrs:
                if attrName == "value" and attrValue == "Add to Cart":
                    self.in_stock = True
        if self.price == -1.0 and tag == "span":
            for attrName, attrValue in attrs:
                if attrName == "id" and attrValue == "price_inside_buybox":
                    self.next_data_price = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.next_data_price:
            self.price = float(data.strip()[1:])
            self.next_data_price = False

    def feed(self, data):
        super().feed(data)
        return self.price, self.in_stock


class ItemCondition(Enum):
    NEW = "new"
    USED = "used"


class ItemPreference:

    def __init__(self, max_price: int, condition: ItemCondition):
        self.max_price = max_price
        self.condition = condition

    def matches(self, price, condition: ItemCondition) -> bool:
        if self.condition is not None and self.condition != condition:
            return False

        return self.max_price is None or price <= self.max_price


def ini_to_item(ini_str: str):
    parts = ini_str.split("|")

    if len(parts) == 1:
        return parts[0], ItemPreference()
    elif len(parts) == 2:
        if parts[1].replace(".", "", 1).isnumeric():
            return parts[0], ItemPreference(max_price=float(parts[1]))
        return parts[0], ItemPreference(condition=ItemCondition(parts[1]))

    return parts[0], ItemPreference(max_price=float(parts[1]), condition=ItemCondition(parts[2]))


class Amazon(AbstractStore):
    sku_to_max_price = {}

    def __init__(self):
        self.custom_headers = amazonHeaders
        self.item_preferences = {}

    def item_to_sku(self, item):
        # BestBuy items are skus themselves
        sku, preference = ini_to_item(item)
        self.item_preferences[sku] = preference
        return sku

    def sku_to_url(self, sku: str) -> str:
        return "https://www.amazon.com/gp/product/{}".format(sku)

    def is_in_stock(self, sku, data: str) -> bool:
        price, in_stock = AmazonParser().feed(data)
        item_preference = self.item_preferences[sku]

        # Assume all are new for now
        return in_stock and item_preference.matches(price, ItemCondition.NEW)
