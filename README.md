The purpose of this repository is to alert you when an item comes into stock.

Currently, there is support for Bestbuy, Staples, Newegg, and EVGA. Delays between queries to various stores is independent.

For every individual store, there are currently two configuration options. Within the store's category in the `config.ini` file, there is the `items` field and the `delay` field. For the `delay` field, simply set the duration in seconds you would like the script to sleep in between requests for that specific store. Below you will find the configuration options for the `items` field for each store.

## BestBuy

For BestBuy, the `items` field simply indicates a comma delimited list of product SKUs.

## Staples

For Staples, the `items` field simply indicates a comma delimited list of product numbers.

## Newegg

For Newegg, the `items` field simply indicates a comma delimited list of item numbers.

## EVGA

For EVGA, the `items` field simply indicates a comma delimited list of product numbers.

On top of these stores, it is also currently possible to configure SMS alerts. To do so, configure a queue in AWS SNS via [this guide](https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html). When configuring a subscription, choose SMS instead of email and use the phone number you wish to be notified at. Then, navigate to your created SNS Topic and grab the resource ARN. Specify this ARN in the `config.ini` under `[notifier]`, using the field `sns_topic_arn`.