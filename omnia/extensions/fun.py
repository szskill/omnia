import time

from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


class Fun(commands.Cog):
    """Cogs for fun!"""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.command(aliases=["latency"])
    async def ping(self, ctx: commands.Context) -> None:
        """🏓 Pong!"""

        start = time.time_ns()
        await ctx.trigger_typing()
        stop = time.time_ns()
        latency_ms = round((stop - start) / 1_000_000)

        embed = FancyEmbed(
            ctx=ctx,
            title="🏓 Pong!",
            description=f"Latency: {latency_ms}ms",
            color=self.bot.primary_color,
        )

        await ctx.reply(embed=embed)


def setup(bot: Omnia) -> None:
    """Loads the `Fun` cog."""
    bot.add_cog(Fun(bot))
