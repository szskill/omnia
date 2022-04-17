import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


def get_tags_key(ctx: commands.Context) -> str:
    """Gets the tags key of a guild."""

    assert ctx.guild is not None
    return f"{ctx.bot.redis_keyspace}.guilds.{ctx.guild.id}.tags"


class Tags(commands.Cog):
    """The cog for tags."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx: commands.Context, name: str) -> None:
        """Shows you a tag."""

        if ctx.guild is None:
            return

        text = await self.bot.redis_db.hget(get_tags_key(ctx), name)

        if not text:
            await ctx.reply(f"The tag with name `{name}` does not exist.")
            return

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"Tag `{name}`",
                description=text,
                color=self.bot.primary_color,
            )
        )

    @tag.command()
    @commands.has_permissions(manage_messages=True)
    async def create(self, ctx: commands.Context, name: str, *, text: str) -> None:
        """Creates a tag only for this server."""

        if ctx.guild is None:
            return

        tag_key = get_tags_key(ctx)

        tags = await self.bot.redis_db.hgetall(tag_key)

        if name in tags:
            await ctx.reply(
                f"A tag with the name `{name}` already exists in this server."
            )
            return

        await self.bot.redis_db.hset(tag_key, name, text)

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="✅ Created tag",
                description=f"Created tag `{name}` with text `{text}`",
                color=disnake.Color.brand_green(),
            )
        )

    @tag.command(name="list")
    async def list_(self, ctx: commands.Context) -> None:
        """Lists all of the tags in this server."""

        if not ctx.guild:
            return

        tag_key = get_tags_key(ctx)

        tags: dict = await self.bot.redis_db.hgetall(tag_key)

        if not tags:
            await ctx.reply(
                embed=FancyEmbed(
                    ctx=ctx,
                    title="This server has no tags",
                    description=(
                        f"Change that by doing `{ctx.clean_prefix}tag create <name>"
                        + " <text>`"
                    ),
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"✅ Tags for `{ctx.guild}`",
                description=", ".join(tags.keys()),
                color=self.bot.primary_color,
            )
        )

    @tag.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx: commands.Context, name: str) -> None:
        """Deletes a tag."""

        if ctx.guild is None:
            return

        await self.bot.redis_db.hdel(get_tags_key(ctx), name)

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=f"✅ Deleted tag `{name}`",
                description="Goodbye, tag!",
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `Tags` cog."""
    bot.add_cog(Tags(bot))
