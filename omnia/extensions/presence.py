import disnake
from disnake.ext import commands

from omnia.omnia import Omnia


class Presence(commands.Cog):
    """The cog that sets up rich presence."""

    def __init__(self, bot: Omnia) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            activity=disnake.Game(self.bot.statuses[0]),
            status=disnake.Status.do_not_disturb,
        )


def setup(bot: commands.Bot) -> None:
    """Loads the `Presence` cog."""
    bot.add_cog(Presence(bot))
