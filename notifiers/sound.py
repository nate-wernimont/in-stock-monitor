import os
from notifiers.abstract import AbstractNotifier


class SoundNotifier(AbstractNotifier):

    def __init__(self, freq, duration):
        self.freq = freq
        self.duration = duration

    async def notify(self, url):
        os.system(
            'play -nq -t alsa synth {} sine {}'.format(self.duration, self.freq))
