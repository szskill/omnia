import datetime

import disnake


class FancyEmbed(disnake.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp = datetime.datetime.now()
