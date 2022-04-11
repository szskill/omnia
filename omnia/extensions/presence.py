import random

import disnake
from disnake.ext import commands, tasks

from ..omnia import Omnia


class Presence(commands.Cog):
    """The cog that sets up rich presence."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @tasks.loop(seconds=30)
    async def change_status(self) -> None:
        await self.bot.change_presence(
            activity=disnake.Game(random.choice(self.bot.statuses)),
            status=disnake.Status.do_not_disturb,
        )

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.change_status.start()


def setup(bot: Omnia) -> None:
    """Loads the `Presence` cog."""
    bot.add_cog(Presence(bot))
