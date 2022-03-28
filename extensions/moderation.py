import disnake
from disnake.ext import commands


class Moderation(commands.Cog):
    """The cog for moderation. Moderation cog. Moderational cog. Kick ban cog."""

    def __init__(self) -> None:
        super().__init__()

    @commands.command()
    async def kick(
        self,
        ctx: commands.Context,
        member: disnake.Member,
        *,
        reason: str = "no reason",
    ) -> None:
        """Kicks a member from a server."""

        if ctx.author == member:
            return await ctx.reply("😔 I'm too nice to kick you.")
        elif ctx.author == ctx.bot:
            return await ctx.reply("🤨 Why?")

        await member.kick(reason=reason)
        await ctx.reply(f"Kicked `{member}` for `{reason}`")

    @commands.command()
    async def ban(
        self,
        ctx: commands.Context,
        member: disnake.Member,
        *,
        reason: str = "no reason",
    ) -> None:
        """Bans a member from a server."""

        if ctx.author == member:
            return await ctx.reply("😔 I'm too nice to ban you.")
        elif ctx.author == ctx.bot:
            return await ctx.reply("🤨 Why?")

        await member.ban(reason=reason)
        await ctx.reply(f"Banned `{member}` for `{reason}`")


def setup(bot: commands.Bot) -> None:
    """Loads the `Moderation` cog."""
    bot.add_cog(Moderation())
