"""Entrypoint for Omnia."""

import logging
from os import getenv

from dotenv import load_dotenv

from omnia.omnia import Omnia


def setup_logging() -> None:
    """Sets up logging."""

    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


if __name__ == "__main__":
    load_dotenv()
    setup_logging()

    Omnia().run(getenv("TOKEN"))
