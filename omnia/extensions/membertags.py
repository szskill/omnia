import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


def get_membertag_key(ctx: commands.Context, member: disnake.Member) -> str:
    """Returns the membertag key for a member."""

    assert ctx.guild is not None
    return f"{ctx.bot.redis_keyspace}.guilds.{ctx.guild.id}.members.{member.id}.tags"


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
            get_membertag_key(ctx, member),
            name,
        )

        if not text:
            await ctx.reply(
                f"The tag with name `{name}` for that member does not exist."
            )
            return

        await ctx.reply(
            embed=FancyEmbed(
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
            get_membertag_key(ctx, member),
            name,
            text,
        )

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="✅ Set tag",
                description=f"Set tag `{name}` for {member.mention} with text `{text}`",
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `MemberTags` cog."""
    bot.add_cog(MemberTags(bot))
