import logging

import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed

ERROR_TITLE_MAP = {
    commands.MissingPermissions: "❌ Missing permissions",
    commands.BotMissingPermissions: "❌ I'm missing permissions",
    commands.MissingRequiredArgument: "❌ Missing required argument",
    commands.BadArgument: "❌ Bad argument",
    commands.CheckFailure: "❌ Check failed",
    commands.CommandOnCooldown: "❌ Command on cooldown",
    commands.MemberNotFound: "❌ Member not found",
    commands.CommandInvokeError: "❌ Command invoke error",
    commands.CommandError: "❌ Unknown error",
}

ERROR_DESCRIPTION_MAP = {
    commands.MissingPermissions: "You're missing permissions to do that.",
    commands.BotMissingPermissions: "I'm missing permissions to do that.",
    commands.MissingRequiredArgument: "You're missing a required argument.",
    commands.BadArgument: "You gave an invalid argument.",
    commands.CheckFailure: "You failed a check.",
    commands.CommandOnCooldown: "That command is on cooldown.",
    commands.MemberNotFound: "I couldn't find that member.",
    commands.CommandInvokeError: "An error occurred while invoking the command.",
    commands.CommandError: "An unknown error occurred.",
}


class ErrorHandling(commands.Cog):
    """The cog that handles errors."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        # Check if the title map doesn't have the error's name
        if type(error) not in ERROR_TITLE_MAP.keys() and ctx.command is not None:
            logging.warn(
                f"Unhandled error {type(error).__name__} on command {ctx.command.name}:"
                + f" \n{error}"
            )
            await self.bot.redis_db.incr(
                f"{self.bot.redis_keyspace}.command_errors.{ctx.command.name}"
            )

        # Choose the title and description from ERROR_TITLE_MAP and provide default
        # values
        title = [t for err, t in ERROR_TITLE_MAP.items() if isinstance(error, err)][0]
        description = [
            desc
            for err, desc in ERROR_DESCRIPTION_MAP.items()
            if isinstance(error, err)
        ][0]

        await ctx.reply(
            embed=FancyEmbed(
                ctx=ctx,
                title=title,
                description=description,
                color=disnake.Color.brand_red(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `ErrorHandling` cog."""
    bot.add_cog(ErrorHandling(bot))
