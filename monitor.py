import asyncio
from stores.interface.interface import AbstractStore
from stores.interface.interface import AbstractBuyableStore
import requests
from requests.exceptions import ConnectionError


class Monitor:

    def __init__(self, store: AbstractStore, items, notifiers):
        self.store = store
        self.items = items
        self.texted_links = {}
        self.notifiers = notifiers

    async def run(self, delay: int):
        skus = map(lambda item: self.store.item_to_sku(item), self.items)

        skus_to_urls = dict((sku, self.store.sku_to_url(sku))
                            for sku in skus)

        while True:
            for sku, url in skus_to_urls.items():
                await asyncio.sleep(delay)

                try:
                    response = requests.get(
                        url, headers=self.store.custom_headers)
                except ConnectionError:
                    continue
                if response.status_code != 200:
                    print("unable to request data for url: {}".format(url))
                    continue

                in_stock = self.store.is_in_stock(
                    sku, response.content.decode("utf-8"))
                if in_stock:
                    if self.store is AbstractBuyableStore:
                        self.store.buy_item(sku)
                    for notifier in self.notifiers:
                        notifier.notify(url)
                else:
                    print("Out of stock: {}".format(sku))
