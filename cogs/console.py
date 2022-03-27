import rich
from disnake.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omnia import Omnia


class Console(commands.Cog):
    """The cog that informs you of bot events in the console."""

    INIT_EXTRA_ARGS = ("bot",)

    def __init__(self, bot: "Omnia") -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        rich.print(
            "[b]🤖 Omnia is ready![/b]\n"
            + f"| [gray]Version:[/gray] [aqua]{self.bot.version}[/aqua]\n"
            + f"| [gray]Prefix:[/gray] [aqua]{self.bot.command_prefix}[/aqua]"
        )
