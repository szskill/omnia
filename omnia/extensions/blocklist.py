import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed


def get_blocklist_key(bot: Omnia, guild: disnake.Guild) -> str:
    """Returns the blocklist key for a guild."""
    return f"{bot.redis_keyspace}.guilds.{guild.id}.blocklist"


class Blocklist(commands.Cog):
    """The cog for managing command blocklists."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot
        self.bot.event(self.on_message)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def blocklist(self, ctx: commands.Context, command_name: str) -> None:
        """Blocks a command from the server."""

        if ctx.guild is None:
            return

        # Make it case-insensitive
        command_name = command_name.lower()

        # We don't want users being able to not control blocklists
        if command_name == "unblocklist":
            await ctx.reply("`unblocklist` is simply too.. cool to get blocklisted ๐")
            return

        blocklist_key = get_blocklist_key(self.bot, ctx.guild)

        if not await self.bot.redis_db.exists(blocklist_key):
            await self.bot.redis_db.sadd(blocklist_key, " ")  # to initialize blocklist

        already_blocklisted = await self.bot.redis_db.smembers(blocklist_key)

        if command_name in already_blocklisted:
            await ctx.reply(
                embed=FancyEmbed(
                    ctx=ctx,
                    title="๐คจ Already blocklisted!",
                    description=f"`{command_name}` is already blocklisted.",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await self.bot.redis_db.sadd(blocklist_key, command_name)

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="โ Blocklisted!",
                description=f"`{command_name}` has been blocklisted.",
                color=disnake.Color.brand_green(),
            )
        )

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unblocklist(self, ctx: commands.Context, command_name: str) -> None:
        """Unblocks a command from the server."""

        if ctx.guild is None:
            return

        blocklist_key = get_blocklist_key(self.bot, ctx.guild)

        if not await self.bot.redis_db.exists(blocklist_key):
            await self.bot.redis_db.sadd(blocklist_key, " ")  # to initialize blocklist

        already_blocklisted = await self.bot.redis_db.smembers(blocklist_key)

        if command_name not in already_blocklisted:
            await ctx.reply(
                embed=FancyEmbed(
                    ctx=ctx,
                    title="๐คจ Not blocklisted!",
                    description=f"`{command_name}` is not blocklisted.",
                    color=disnake.Color.brand_red(),
                )
            )
            return

        await self.bot.redis_db.srem(blocklist_key, command_name)

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="โ Unblocklisted!",
                description=f"`{command_name}` has been unblocklisted.",
                color=disnake.Color.brand_green(),
            )
        )

    async def on_message(self, message: disnake.Message) -> None:
        """Checks if a blocked command is attempting to be used."""

        if message.guild is None:
            return

        blocklist = await self.bot.redis_db.smembers(
            get_blocklist_key(self.bot, message.guild)
        )

        if not blocklist:
            await self.bot.process_commands(message)
            return

        if message.content.startswith(self.bot.command_prefix):
            command_name = message.content.split(self.bot.command_prefix)[1].split()[0]

            if command_name in blocklist:
                await message.reply(
                    embed=FancyEmbed(
                        title="โ Not allowed",
                        description=f"`{command_name}` is not allowed in this server.",
                        color=disnake.Color.brand_red(),
                    )
                )
                return

        # We have to call process_commands so the commands will be executed
        await self.bot.process_commands(message)


def setup(bot: Omnia) -> None:
    """Loads the `Blocklist` cog."""
    bot.add_cog(Blocklist(bot))
