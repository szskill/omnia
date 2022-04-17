import datetime

import disnake
from disnake.ext.commands import Context


class FancyEmbed(disnake.Embed):
    def __init__(self, *args, ctx: Context | None = None, **kwargs):
        self.timestamp = datetime.datetime.now()

        if ctx is not None:
            self.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )

        super().__init__(*args, **kwargs)
