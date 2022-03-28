from os import getenv
from dotenv import load_dotenv
from omnia.omnia import Omnia

if __name__ == "__main__":
    load_dotenv()
    Omnia().run(getenv("TOKEN"))
