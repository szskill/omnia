import logging

import disnake
from disnake.ext import commands

from ..omnia import Omnia
from ..fancy_embed import FancyEmbed

ERROR_TITLE_MAP = {
    "MissingPermissions": "❌ Missing permissions",
    "BotMissingPermissions": "❌ I'm missing permissions",
    "MissingRequiredArgument": "❌ Missing required argument",
    "BadArgument": "❌ Bad argument",
    "CheckFailure": "❌ Check failed",
    "CommandOnCooldown": "❌ Command on cooldown",
    "MemberNotFound": "❌ Member not found",
    "CommandInvokeError": "❌ Command invoke error",
    "CommandError": "❌ Unknown error",
}

ERROR_DESCRIPTION_MAP = {
    "MissingPermissions": "You're missing permissions to do that.",
    "BotMissingPermissions": "I'm missing permissions to do that.",
    "MissingRequiredArgument": "You're missing a required argument.",
    "BadArgument": "You gave an invalid argument.",
    "CheckFailure": "You failed a check.",
    "CommandOnCooldown": "That command is on cooldown.",
    "MemberNotFound": "I couldn't find that member.",
    "CommandInvokeError": "An error occurred while invoking the command.",
    "CommandError": "An unknown error occurred.",
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
        if (
            type(error).__name__ not in ERROR_TITLE_MAP.keys()
            and ctx.command is not None
        ):
            logging.warn(
                f"Unhandled error {type(error).__name__} on command {ctx.command.name}:"
                + f" \n{error}"
            )
            await self.bot.redis_db.incr(
                f"{self.bot.redis_keyspace}.command_errors.{ctx.command.name}"
            )

        # Choose the title and description from ERROR_TITLE_MAP and provide default
        # values
        title = ERROR_TITLE_MAP.get(type(error).__name__, "❌ Unknown error")
        description = ERROR_DESCRIPTION_MAP.get(
            type(error).__name__, f"```\n{error}\n```"
        )

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
