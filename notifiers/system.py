import desktop_notify
from notifiers.abstract import AbstractNotifier


class SystemNotifier(AbstractNotifier):

    async def notify(self, url: str):
        notify = desktop_notify.aio.Notify("In Stock", url)
        notify.set_timeout(30000)
        await notify.show()
