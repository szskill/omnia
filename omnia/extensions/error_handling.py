import logging

import disnake
from disnake.ext import commands

from omnia.omnia import Omnia


class ErrorHandling(commands.Cog):
    """The cog that handles errors."""

    def __init__(self, bot: Omnia) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing Permissions",
                    description="You do not have permission to perform this command.",
                    color=disnake.Color.brand_red(),
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=disnake.Embed(
                    title="Missing Required Argument",
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
            await self.bot.redis_db.incr(f"omnia.command_errors.{ctx.command.name}")


def setup(bot: commands.Bot) -> None:
    """Loads the `ErrorHandling` cog."""
    bot.add_cog(ErrorHandling(bot))
