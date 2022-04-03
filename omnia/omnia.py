from os import listdir
import disnake

import yaml
import aioredis
from fakeredis import aioredis as fake_aioredis
from disnake.ext import commands


class Omnia(commands.Bot):
    """THE bot!"""

    def __init__(self) -> None:
        super().__init__()

        self.case_insensitive = True

        self.version = ""
        self.statuses = []
        self.enabled_extensions = []
        self.redis_port = 0
        self.use_fake_redis = False
        self.primary_color = 0x000000

        self.redis_db: aioredis.Redis = None
        self.redis_keyspace: str = "omnia"

        self._read_from_config_file()
        self._register_extensions()
        self._connect_to_databases()

    def _read_from_config_file(self, file: str = "config.yaml") -> None:
        """Reads configuration from a `config.yaml` file."""

        with open(file) as file:
            config = yaml.load(file, yaml.FullLoader)

            self.command_prefix = config["prefix"]
            self.version = config["version"]
            self.statuses = config["statuses"]
            self.enabled_extensions = config["enabled-extensions"]
            self.redis_port = config["redis-port"]
            self.use_fake_redis = config["use-fake-redis"]
            self.primary_color = disnake.Color(int(config["primary-color"]))

    def _register_extensions(self) -> None:
        """Registers all extensions from `self.enabled_extensions`."""

        for extension in listdir("omnia/extensions"):
            name = extension.removesuffix(".py")

            if extension.endswith(".py") and name in self.enabled_extensions:
                self.load_extension(f"omnia.extensions.{name}")

    def _connect_to_databases(self) -> None:
        """Connects to the required databases."""

        if self.use_fake_redis:
            self.redis_db = fake_aioredis.FakeRedis(
                port=self.redis_port, decode_responses=True
            )
        else:
            self.redis_db = aioredis.Redis(port=self.redis_port, decode_responses=True)
