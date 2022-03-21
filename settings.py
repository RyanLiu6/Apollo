import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

DISCORD_PREFIX = os.environ.get("prefix")
DISCORD_TOKEN = os.environ.get("token")

SPOTIFY_ID = os.environ.get("client_id")
SPOTIFY_SECRET = os.environ.get("client_secret")
