The purpose of this repository is to alert you when an item comes into stock.

Currently, there is support for both Staples and BestBuy. Delays between queries to various stores is independent.

## BestBuy

In order to configure the settings for BestBuy, you can modify the `config.ini` file. Under `[bestbuy]`, set the `skus` field to a comma delimited list of product SKUs. You can also modify the `delay`, which is the amount of time in between queries to BestBuy.

## Staples

In order to configure the settings for Staples, you can modify the `config.ini` file. Under `[staples]`, set the `skus` field to a comma delimited list of product SKUs. You can also modify the `delay`, which is the amount of time in between queries to Staples.

On top of these stores, it is also currently possible 