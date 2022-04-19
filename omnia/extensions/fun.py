import time

from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


def stutter(s: str) -> str:
    """Stutters the first letter of a string."""
    return s[0] + "- " + s


class Fun(commands.Cog):
    """Cogs for fun!"""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.command(aliases=["latency"])
    async def ping(self, ctx: commands.Context) -> None:
        """🏓 Pong!"""

        # Calculate the time it took for ctx.trigger_typing to finish
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

    @commands.command(aliases=["uwu"])
    async def uwuify(self, ctx: commands.Context, *, text: str) -> None:
        """o- omnia can awso uwuify text UwU"""

        # Example:
        #   The quick brown fox jumps over the lazy dog.
        #   t- the quick bwown fox jumps ovew the lazy dog....
        uwu_text = stutter(text.lower()).replace("r", "w") + "..."

        await ctx.send(f"> {uwu_text}")


def setup(bot: Omnia) -> None:
    """Loads the `Fun` cog."""
    bot.add_cog(Fun(bot))
