import hashlib
import logging

import disnake
from disnake.ext import commands


def sha1_hash(s: str) -> None:
    """Returns the SHA-1 hash of a string."""
    return hashlib.sha1(s.encode()).hexdigest()


class Tickets(commands.Cog):
    """The cog for tickets."""

    def __init__(self) -> None:
        self.members_with_tickets = []

    @commands.group()
    async def ticket(self, _) -> None:
        pass

    @ticket.command()
    async def create(self, ctx: commands.Context) -> None:
        """Creates a ticket."""

        if ctx.author.id in self.members_with_tickets:
            return await ctx.reply("You've already opened a ticket.")

        channel_name = f"ticket-{sha1_hash(str(ctx.author.id))[:6]}"

        channel = await ctx.guild.create_text_channel(channel_name)

        self.members_with_tickets.append(ctx.author.id)

        await ctx.reply(
            embed=disnake.Embed(
                title="Ticket created",
                description=channel.mention,
                color=disnake.Color.brand_green(),
            )
        )

    @ticket.command()
    async def close(self, ctx: commands.Context) -> None:
        """Closes a ticket."""

        if (
            ctx.channel.name != f"ticket-{sha1_hash(str(ctx.author.id))[:6]}"
            and not ctx.author.guild_permissions.manage_channels
        ):
            return await ctx.reply("This channel isn't yours.")

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
