import disnake
from disnake.ext import commands


class Fun(commands.Cog):
    """Cogs for fun!"""

    def __init__(self) -> None:
        super().__init__()

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        embed = disnake.Embed(
            title=":ping_pong: Pong!",
            description=f"This is Omnia version {ctx.bot.version}!",
        )

        await ctx.reply(embed=embed)
