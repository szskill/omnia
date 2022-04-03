import logging

import disnake
from disnake.ext import commands

from ..omnia import Omnia


class ErrorHandling(commands.Cog):
    """The cog that handles errors."""

    def __init__(self, bot: Omnia) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing permissions",
                    description="You do not have permission to perform this command.",
                    color=disnake.Color.brand_red(),
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing required argument",
                    description=f"You are missing the `{error.param.name}` argument",
                    color=disnake.Color.brand_red(),
                )
            )
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            logging.warn(
                f"Unhandled error {error.__class__} on command {ctx.command.name}"
            )
            await self.bot.redis_db.incr(
                f"{self.bot.redis_keyspace}.command_errors.{ctx.command.name}"
            )

            await ctx.reply(
                embed=disnake.Embed(
                    title="Unknown error",
                    description=f"```\n{error}\n```",
                    color=disnake.Color.brand_red(),
                )
            )


def setup(bot: commands.Bot) -> None:
    """Loads the `ErrorHandling` cog."""
    bot.add_cog(ErrorHandling(bot))
