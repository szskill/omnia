import disnake
from disnake.ext import commands

from omnia.omnia import Omnia


class Tag(commands.Cog):
    """The cog for tags."""

    def __init__(self, bot: Omnia) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name="create-tag")
    @commands.has_permissions(manage_messages=True)
    async def create_tag(self, ctx: commands.Context, name: str, *, text: str) -> None:
        """Creates a tag only for this server."""

        tag_key = f"{self.bot.redis_keyspace}.guild.{ctx.guild.id}.tags.{name}"

        if tag_key in await self.bot.redis_db.keys():
            return await ctx.reply(
                f"A tag with the name `{name}` already exists in this server."
            )

        await self.bot.redis_db.set(tag_key, text)

        await ctx.reply(
            embed=disnake.Embed(
                title="Created Tag",
                description=f"Created tag `{name}` with text `{text}`",
                color=disnake.Color.brand_green(),
            )
        )

    @commands.command(aliases=("get-tag", "display-tag", "show-tag"))
    async def tag(self, ctx: commands.Context, name: str) -> None:
        """Shows you a tag."""

        text = await self.bot.redis_db.get(
            f"{self.bot.redis_keyspace}.guild.{ctx.guild.id}.tags.{name}"
        )

        if not text:
            return await ctx.reply(f"The tag with name `{name}` does not exist.")

        await ctx.reply(
            embed=disnake.Embed(
                title=f"Tag `{name}`", description=text, color=disnake.Color.random()
            )
        )

    @commands.command(name="delete-tag")
    @commands.has_permissions(manage_messages=True)
    async def delete_tag(self, ctx: commands.Context, name: str) -> None:
        await self.bot.redis_db.delete(
            f"{self.bot.redis_keyspace}.guild.{ctx.guild.id}.tags.{name}"
        )

        await ctx.reply(
            embed=disnake.Embed(
                title=f"Deleted Tag `{name}`",
                description="Goodbye, tag!",
                color=disnake.Color.brand_green(),
            )
        )


def setup(bot: commands.Bot) -> None:
    """Loads the `Tag` cog."""
    bot.add_cog(Tag(bot))
