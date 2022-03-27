import yaml
from disnake.ext import commands

import cogs


class Omnia(commands.Bot):
    """THE bot!"""

    def __init__(self) -> None:
        super().__init__()

        self.version = ""
        self.statuses = []
        self.enabled_cogs = []

        self._read_from_config_file()
        self._register_cogs()

    def _read_from_config_file(self, file: str = "config.yaml") -> None:
        """Reads configuration from a `config.yaml` file."""

        with open(file) as file:
            config = yaml.load(file, yaml.FullLoader)

            self.command_prefix = config["prefix"]
            self.version = config["version"]
            self.statuses = config["statuses"]
            self.enabled_cogs = config["enabled-cogs"]

    def _register_cogs(self) -> None:
        """Registers all cogs from `self.enabled_cogs`."""

        for Cog in cogs.all_cogs:
            if Cog.__cog_name__.lower() in self.enabled_cogs:
                if hasattr(Cog, "INIT_EXTRA_ARGS"):
                    args = []
                    for extra_arg in Cog.INIT_EXTRA_ARGS:
                        if extra_arg == "bot":
                            args.append(self)
                    self.add_cog(Cog(*args))
                else:
                    self.add_cog(Cog())
