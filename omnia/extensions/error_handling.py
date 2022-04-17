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
    "CommandInvokeError": "❌ Command invoke error",
    "MemberNotFound": "❌ Member not found",
    "CommandError": "❌ Unknown error",
}

ERROR_DESCRIPTION_MAP = {
    "MissingPermissions": "You're missing permissions to do that.",
    "BotMissingPermissions": "I'm missing permissions to do that.",
    "MissingRequiredArgument": "You're missing a required argument.",
    "BadArgument": "You gave an invalid argument.",
    "CheckFailure": "You failed a check.",
    "CommandOnCooldown": "That command is on cooldown.",
    "CommandInvokeError": "An error occurred while invoking the command.",
    "MemberNotFound": "I couldn't find that member.",
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
        elif type(error) not in ERROR_TITLE_MAP.keys() and ctx.command is not None:
            logging.warn(
                f"Unhandled error {type(error).__name__} on command {ctx.command.name}"
            )
            await self.bot.redis_db.incr(
                f"{self.bot.redis_keyspace}.command_errors.{ctx.command.name}"
            )

        await ctx.reply(
            embed=FancyEmbed(
                title=ERROR_TITLE_MAP.get(type(error).__name__, "❌ Unknown error"),
                description=ERROR_DESCRIPTION_MAP.get(
                    type(error).__name__, f"```\n{error}\n```"
                ),
                color=disnake.Color.brand_red(),
            )
        )


def setup(bot: Omnia) -> None:
    """Loads the `ErrorHandling` cog."""
    bot.add_cog(ErrorHandling(bot))
