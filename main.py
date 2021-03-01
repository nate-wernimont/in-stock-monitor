import asyncio
import configparser
import sys
import time

from monitor import Monitor
from stores.bestbuy import BestBuy
from stores.evga import EVGA
from stores.newegg import Newegg
from stores.staples import Staples
from stores.amazon import Amazon
from notifiers.sms import SMSNotifier
from notifiers.system import SystemNotifier

# The amount of time to sleep between requests
REQUEST_DELAY = 5
ITEM_LIST_CONFIG_NAME = "items"
DELAY_CONFIG_NAME = "delay"
NOTIFIER_CONFIG_CATEGORY = "notifier"
SNS_TOPIC_NAME = "sns_topic_arn"
CONFIG_FILE = "config.ini"


async def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    tasks = []

    notifiers = [SystemNotifier()]

    sns_topic = config[NOTIFIER_CONFIG_CATEGORY][SNS_TOPIC_NAME]
    if sns_topic is not None:
        notifiers.append(SMSNotifier(sns_topic=sns_topic))

    storesToInitializers = {
        'bestbuy': BestBuy,
        'staples': Staples,
        'newegg': Newegg,
        'evga': EVGA,
        'amazon': Amazon,
    }

    for storeName, storeInit in storesToInitializers.items():
        if storeName not in config:
            continue
        storeConfig = config[storeName]

        items = set(storeConfig[ITEM_LIST_CONFIG_NAME].split(","))
        delay = REQUEST_DELAY
        if DELAY_CONFIG_NAME in storeConfig:
            delay = storeConfig[DELAY_CONFIG_NAME]

        tasks.append(asyncio.create_task(
            Monitor(
                store=storeInit(),
                items=items,
                notifiers=notifiers
            ).run(delay=int(delay))))

    await asyncio.gather(*tasks)

asyncio.run(main())
