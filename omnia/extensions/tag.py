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

        await self.bot.redis_db.set(
            f"{self.bot.redis_keyspace}.guild.{ctx.guild.id}.tags.{name}", text
        )

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


def setup(bot: commands.Bot) -> None:
    """Loads the `Tag` cog."""
    bot.add_cog(Tag(bot))
