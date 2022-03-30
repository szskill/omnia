import disnake
from disnake.ext import commands


class Fun(commands.Cog):
    """Cogs for fun!"""

    def __init__(self) -> None:
        super().__init__()

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """🏓 Pong!"""

        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"This is Omnia version {ctx.bot.version}!",
            color=disnake.Color.random(),
        )

        await ctx.reply(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Loads the `Fun` cog."""
    bot.add_cog(Fun())
