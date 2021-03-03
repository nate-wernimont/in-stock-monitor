import asyncio
from configobj import ConfigObj

from monitor import Monitor
from stores.bestbuy import BestBuy
from stores.evga import EVGA
from stores.newegg import Newegg
from stores.staples import Staples
from stores.amazon import Amazon
from notifiers.sms import SMSNotifier
from notifiers.system import SystemNotifier
from notifiers.sound import SoundNotifier

# The amount of time to sleep between requests
REQUEST_DELAY = 5
ITEM_LIST_CONFIG_NAME = "items"
DELAY_CONFIG_NAME = "delay"
NOTIFIER_CONFIG_CATEGORY = "notifier"
SNS_TOPIC_NAME = "sns_topic_arn"
CONFIG_FILE = "config.ini"
EXTRA_CONFIG_NAME = "extra"
FREQUENCY_NAME = "freq"
DURATION_NAME = "duration"


async def main():
    config = ConfigObj(CONFIG_FILE, list_values=False)
    tasks = []

    notifiers = [SystemNotifier()]

    if NOTIFIER_CONFIG_CATEGORY in config:
        notifier_config = config[NOTIFIER_CONFIG_CATEGORY]
        if SNS_TOPIC_NAME in notifier_config:
            notifiers.append(SMSNotifier(
                sns_topic=notifier_config[SNS_TOPIC_NAME]))
        if FREQUENCY_NAME in notifier_config and DURATION_NAME in notifier_config:
            notifiers.append(SoundNotifier(
                freq=notifier_config[FREQUENCY_NAME], duration=notifier_config[DURATION_NAME]))

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
            delay = int(storeConfig[DELAY_CONFIG_NAME])

        extraConfig = {}
        if EXTRA_CONFIG_NAME in storeConfig:
            extraConfig = storeConfig[EXTRA_CONFIG_NAME]

        tasks.append(asyncio.create_task(
            Monitor(
                store=storeInit(config=extraConfig),
                items=items,
                notifiers=notifiers
            ).run(delay=int(delay))))

    await asyncio.gather(*tasks)

asyncio.run(main())
