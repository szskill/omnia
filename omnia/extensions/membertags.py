import disnake
from disnake.ext import commands

from ..omnia import Omnia


class MemberTags(commands.Cog):
    """The cog for membertags."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def membertag(
        self, ctx: commands.Context, member: disnake.Member, name: str
    ) -> None:
        """Fetches a tag of a member."""

        if ctx.guild is None:
            return

        text = await self.bot.redis_db.hget(
            f"{self.bot.redis_keyspace}.guilds.{ctx.guild.id}.membertags.{member.id}",
            name,
        )

        if not text:
            await ctx.reply(
                f"The tag with name `{name}` for that member does not exist."
            )
            return

        await ctx.reply(
            embed=disnake.Embed(
                title=f"Tag `{name}` for `{member}`",
                description=text,
                color=self.bot.primary_color,
            )
        )

    @membertag.command()
    @commands.has_permissions(manage_messages=True)
    async def set(
        self, ctx: commands.Context, member: disnake.Member, name: str, *, text: str
    ) -> None:
        """Sets a tag for a member."""

        if ctx.guild is None:
            return

        await self.bot.redis_db.hset(
            f"{self.bot.redis_keyspace}.guilds.{ctx.guild.id}.membertags.{member.id}",
            name,
            text,
        )

        await ctx.reply(
            embed=disnake.Embed(
                title="✅ Set tag",
                description=f"Set tag `{name}` for {member.mention} with text `{text}`",
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `MemberTags` cog."""
    bot.add_cog(MemberTags(bot))
