import time

import disnake
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
        self.last_deleted_message: disnake.Message | None = None

    @commands.command(aliases=["latency"])
    async def ping(self, ctx: commands.Context) -> None:
        """🏓 Pong!"""

        # Calculate the time it took for ctx.trigger_typing to finish
        # This can be any HTTP request to Discord though, not just ctx.trigger_typing.
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

    @commands.command()
    async def snipe(self, ctx: commands.Context) -> None:
        """Snipes the last deleted message."""

        if self.last_deleted_message is None:
            await ctx.reply("I haven't recorded any deleted messages yet.")
            return

        embed = FancyEmbed(
            ctx=ctx,
            title="🔍 Sniped!",
            color=self.bot.primary_color,
        )

        embed.add_field(name="Content", value=self.last_deleted_message.content)
        embed.add_field(name="Author", value=str(self.last_deleted_message.author))
        embed.add_field(name="Channel", value=str(self.last_deleted_message.channel))

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message) -> None:
        """Records the last deleted message."""
        self.last_deleted_message = message


def setup(bot: Omnia) -> None:
    """Loads the `Fun` cog."""
    bot.add_cog(Fun(bot))
