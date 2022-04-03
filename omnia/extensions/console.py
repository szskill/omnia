import rich
from disnake.ext import commands

from ..omnia import Omnia


class Console(commands.Cog):
    """The cog that informs you of bot events in the console."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        rich.print(
            "[b]🤖 Omnia is ready![/b]\n"
            + f"| [gray50]Version:[/gray50] [aqua]{self.bot.version}[/aqua]\n"
            + f"| [gray50]Prefix:[/gray50] [aqua]{self.bot.command_prefix}[/aqua]"
        )


def setup(bot: commands.Bot) -> None:
    """Loads the `Console` cog."""
    bot.add_cog(Console(bot))
