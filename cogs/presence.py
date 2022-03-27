import disnake
from disnake.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omnia import Omnia


class Presence(commands.Cog):
    """The cog that sets up rich presence."""

    INIT_EXTRA_ARGS = ("bot",)

    def __init__(self, bot: "Omnia") -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            activity=disnake.Game(self.bot.statuses[0]),
            status=disnake.Status.do_not_disturb,
        )
