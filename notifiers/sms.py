import boto3
from notifiers.abstract import AbstractNotifier


class SMSNotifier(AbstractNotifier):

    def __init__(self, sns_topic: str):
        self.sns_topic = sns_topic
        self.texted_links = {}

    async def notify(self, url: str):
        if url in self.texted_links:
            return

        client = boto3.client('sns')
        client.publish(
            TopicArn=self.sns_topic,
            Message=url,
        )
        self.texted_links[url] = True
