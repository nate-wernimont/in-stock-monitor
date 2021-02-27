import asyncio
from stores.interface.interface import StoreInterface
import requests
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

class Monitor:

    def __init__(self, store: StoreInterface, skus, sns_topic: str):
        self.store = store
        self.skus = skus
        self.sns_topic = sns_topic
        self.texted_links = {}
    
    async def run(self, delay: int):
        skus_to_urls = dict((sku, self.store.sku_to_url(sku)) for sku in self.skus)

        while True:
            for sku, url in skus_to_urls.items():
                await asyncio.sleep(delay)

                response = requests.get(url, headers=self.store.custom_headers)
                if response.status_code != 200:
                    print("unable to request data for url: {}".format(url))
                    continue

                in_stock = self.store.is_in_stock(response.content.decode("utf-8"))
                if in_stock:
                    self.notify(url)
                else:
                    print("Out of stock: {}".format(sku))
    
    def notify(self, url):
        print(url)
        Notify.init("In Stock Notifier")
        notification = Notify.Notification.new("In Stock", url)
        notification.set_urgency(Notify.Urgency.CRITICAL)
        notification.show()

        if self.sns_topic is None or url in self.texted_links:
            return

        client = boto3.client('sns')
        response = client.publish(
            TopicArn=self.sns_topic,
            Message=url,
        )
        self.texted_links[url] = True