import disnake
from disnake.ext import commands

from ..omnia import Omnia


class Miscellanous(commands.Cog):
    """The cog for all things miscellanous."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.command()
    async def source(self, ctx: commands.Context) -> None:
        """Shows you the link to the source code of Omnia."""

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.link,
                label="Repository",
                url="https://github.com/szskill/omnia",
            )
        )

        await ctx.reply("I'm open source! Check out my GitHub repository:", view=view)


def setup(bot: Omnia) -> None:
    """Loads the `Miscellanous` cog."""
    bot.add_cog(Miscellanous(bot))
