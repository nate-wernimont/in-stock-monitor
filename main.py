import sys
import configparser
import time
import asyncio
from stores.bestbuy import BestBuy
from stores.staples import Staples
from stores.newegg import Newegg
from monitor import Monitor

# The amount of time to sleep between requests
REQUEST_DELAY = 5

async def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    tasks = []

    sns_topic = config['notifier']['sns_topic_arn']

    storesToInitializers = {
        'bestbuy': BestBuy,
        'staples': Staples,
        'newegg': Newegg,
    }

    for storeName, storeInit in storesToInitializers.items():
        storeConfig = config[storeName]
        if storeConfig is None:
            continue

        skus = set(storeConfig['skus'].split(","))
        delay = storeConfig['delay']
        if delay is None:
            delay = REQUEST_DELAY
        
        tasks.append(asyncio.create_task(Monitor(store=storeInit(), skus=skus, sns_topic=sns_topic).run(delay=int(delay))))

    await asyncio.gather(*tasks)

asyncio.run(main())

