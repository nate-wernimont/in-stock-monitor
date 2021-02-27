import gi.repository
import boto3
from urllib3.exceptions import ProtocolError
import asyncio
from stores.interface.interface import AbstractStore
import requests


class Monitor:

    def __init__(self, store: AbstractStore, items, sns_topic: str):
        self.store = store
        self.items = items
        self.sns_topic = sns_topic
        self.texted_links = {}

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
                except:
                    print("Encountered error for: {}".format(sku))
                    continue
                if response.status_code != 200:
                    print("unable to request data for url: {}".format(url))
                    continue

                in_stock = self.store.is_in_stock(
                    sku, response.content.decode("utf-8"))
                if in_stock:
                    print(response.content)
                    self.notify(url)
                else:
                    print("Out of stock: {}".format(sku))

    def notify(self, url):
        print(url)
        repository.Notify.init("In Stock Notifier")
        notification = repository.Notify.Notification.new("In Stock", url)
        notification.set_urgency(repository.Notify.Urgency.CRITICAL)
        notification.show()

        if self.sns_topic is None or url in self.texted_links:
            return

        client = boto3.client('sns')
        response = client.publish(
            TopicArn=self.sns_topic,
            Message=url,
        )
        self.texted_links[url] = True
