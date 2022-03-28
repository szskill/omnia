from os import listdir

import yaml
from disnake.ext import commands


class Omnia(commands.Bot):
    """THE bot!"""

    def __init__(self) -> None:
        super().__init__()

        self.version = ""
        self.statuses = []
        self.enabled_extensions = []

        self._read_from_config_file()
        self._register_extensions()

    def _read_from_config_file(self, file: str = "config.yaml") -> None:
        """Reads configuration from a `config.yaml` file."""

        with open(file) as file:
            config = yaml.load(file, yaml.FullLoader)

            self.command_prefix = config["prefix"]
            self.version = config["version"]
            self.statuses = config["statuses"]
            self.enabled_extensions = config["enabled-extensions"]

    def _register_extensions(self) -> None:
        """Registers all extensions from `self.enabled_extensions`."""

        for extension in listdir("extensions"):
            if extension.endswith(".py"):
                self.load_extension(f"extensions.{extension.removesuffix('.py')}")
