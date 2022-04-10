from typing import Mapping

import disnake
from disnake.ext import commands

from ..omnia import Omnia


# Huge thanks to InterStella0! <3
# https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
class HelpCommand(commands.HelpCommand):
    def __init__(self, primary_color: disnake.Color) -> None:
        super().__init__()
        self.primary_color = primary_color

    def get_command_signature(self, command: commands.Command):
        return (
            f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        )

    async def send_bot_help(self, mapping: Mapping[commands.Cog, commands.Command]):
        embed = disnake.Embed(title="Help", color=self.primary_color)
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures))

        await self.context.reply(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = disnake.Embed(
            title=self.get_command_signature(command), color=self.primary_color
        )

        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias))

        await self.context.reply(embed=embed)

    async def send_group_help(self, group: commands.Group):
        await self.context.reply(
            embed=disnake.Embed(
                title=group.name,
                description="\n".join(
                    list(map(self.get_command_signature, group.commands))
                ),
                color=self.primary_color,
            )
        )

    async def send_error_message(self, error: str):
        await self.context.reply(
            embed=disnake.Embed(
                title="Error", description=error, color=disnake.Color.brand_red()
            )
        )


def setup(bot: Omnia) -> None:
    """Sets the help command to be THIS `HelpCommand`."""

    if isinstance(bot.primary_color, disnake.Color):
        bot.help_command = HelpCommand(bot.primary_color)
