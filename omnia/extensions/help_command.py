from typing import Mapping

import disnake
from disnake.ext import commands


# Huge thanks to InterStella0! <3
# https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
class HelpCommand(commands.HelpCommand):
    def get_command_signature(self, command: commands.Command):
        return (
            f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        )

    async def send_bot_help(self, mapping: Mapping[commands.Cog, commands.Command]):
        embed = disnake.Embed(title="Help", color=disnake.Color.random())
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(
                    name=cog_name, value="\n".join(command_signatures), inline=False
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = disnake.Embed(
            title=self.get_command_signature(command), color=disnake.Color.random()
        )

        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error: str):
        embed = disnake.Embed(
            title="Error", description=error, color=disnake.Color.brand_red()
        )
        channel = self.get_destination()
        await channel.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Sets the help command to be THIS `HelpCommand`."""
    bot.help_command = HelpCommand()
