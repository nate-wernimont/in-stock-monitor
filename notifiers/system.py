import desktop_notify
from notifiers.abstract import AbstractNotifier


class SystemNotifier(AbstractNotifier):

    async def notify(self, url: str):
        await desktop_notify.aio.Notify("In Stock", url).show()
