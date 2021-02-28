from gi.repository import Notify
from notifiers.abstract import AbstractNotifier


class SystemNotifier(AbstractNotifier):

    def notify(self, url: str):
        Notify.init("In Stock Notifier")
        notification = Notify.Notification.new("In Stock", url)
        notification.set_urgency(Notify.Urgency.CRITICAL)
        notification.show()
