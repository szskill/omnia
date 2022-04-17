import datetime

import disnake
from disnake.ext.commands import Context

from .omnia import Omnia


class FancyEmbed(disnake.Embed):
    def __init__(self, *args, ctx: Context | None = None, **kwargs):
        self.timestamp = datetime.datetime.now()

        if ctx is not None:
            self.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )

            if isinstance(ctx.bot, Omnia) and ctx.bot.user.avatar is not None:
                self.set_footer(
                    text=f"Omnia {ctx.bot.version}",
                    icon_url=ctx.bot.user.avatar.url,
                )

        super().__init__(*args, **kwargs)
