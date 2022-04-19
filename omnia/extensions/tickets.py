import hashlib

import disnake
from disnake.ext import commands

from ..fancy_embed import FancyEmbed


def sha1_hash(s: str) -> str:
    """Returns the SHA-1 hash of a string."""
    return hashlib.sha1(s.encode()).hexdigest()


def get_ticket_channel_name(ctx: commands.Context) -> str:
    """Returns the name of the ticket channel."""
    return f"ticket-{sha1_hash(str(ctx.author.id))[:6]}"


def channel_with_name_exists(ctx: commands.Context, name: str) -> bool:
    """Checks if a channel with the name of the ticket channel exists."""

    assert ctx.guild is not None
    return bool([channel for channel in ctx.guild.channels if channel.name == name])


class Tickets(commands.Cog):
    """The cog for tickets."""

    @commands.group()
    async def ticket(self, ctx: commands.Context) -> None:
        """The ticket command group."""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @ticket.command()
    async def create(self, ctx: commands.Context) -> None:
        """Creates a ticket."""

        if ctx.guild is None:
            return

        channel_name = get_ticket_channel_name(ctx)

        if channel_with_name_exists(ctx, channel_name):
            await ctx.reply("You've already opened a ticket.")
            return

        channel = await ctx.guild.create_text_channel(channel_name)
        await channel.set_permissions(
            ctx.author, read_messages=True, send_messages=True  # type: ignore
        )
        await channel.set_permissions(
            ctx.guild.me, read_messages=True, send_messages=True
        )
        await channel.set_permissions(
            ctx.guild.default_role, read_messages=False, send_messages=False
        )

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title="✅ Ticket created",
                description=channel.mention,
                color=disnake.Color.brand_green(),
            )
        )

    @ticket.command()
    async def close(self, ctx: commands.Context) -> None:
        """Closes a ticket."""

        if (
            not ctx.guild
            or not isinstance(ctx.author, disnake.Member)
            or not isinstance(ctx.channel, disnake.TextChannel)
        ):
            return

        if not ctx.channel.name.startswith(
            "ticket-"
        ) and ctx.channel.name != get_ticket_channel_name(ctx):
            await ctx.reply("This channel isn't yours.")
            return

        await ctx.channel.delete()


def setup(bot: commands.Bot) -> None:
    """Loads the `Tickets` cog."""
    bot.add_cog(Tickets())
