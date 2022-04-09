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

        await ctx.reply(
            embed=disnake.Embed(
                title="Omnia's source code",
                description=(
                    "Omnia is open source! Check the code out at"
                    + " <https://github.com/szskill/omnia>! Feel free to contribute or"
                    + " open issues."
                ),
                color=self.bot.primary_color,
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `Miscellanous` cog."""
    bot.add_cog(Miscellanous(bot))
