import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

DISCORD_PREFIX = os.environ.get("discord_prefix")
DISCORD_TOKEN = os.environ.get("discord_token")
