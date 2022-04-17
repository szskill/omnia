import hashlib
import logging

import disnake
from disnake.ext import commands

from ..fancy_embed import FancyEmbed


def sha1_hash(s: str) -> str:
    """Returns the SHA-1 hash of a string."""
    return hashlib.sha1(s.encode()).hexdigest()


class Tickets(commands.Cog):
    """The cog for tickets."""

    def __init__(self) -> None:
        self.members_with_tickets: list[int] = []

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

        if ctx.author.id in self.members_with_tickets:
            await ctx.reply("You've already opened a ticket.")
            return

        channel_name = f"ticket-{sha1_hash(str(ctx.author.id))[:6]}"

        channel = await ctx.guild.create_text_channel(channel_name)

        self.members_with_tickets.append(ctx.author.id)

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

        if (
            ctx.channel.name != f"ticket-{sha1_hash(str(ctx.author.id))[:6]}"
            and not ctx.author.guild_permissions.manage_channels
        ):
            await ctx.reply("This channel isn't yours.")
            return

        try:
            del self.members_with_tickets[
                self.members_with_tickets.index(ctx.author.id)
            ]
        except KeyError:
            logging.warn(
                f"Could not find {ctx.author.id} in members_with_tickets. Did the bot"
                + " restart?"
            )

        await ctx.channel.delete()


def setup(bot: commands.Bot) -> None:
    """Loads the `Tickets` cog."""
    bot.add_cog(Tickets())
