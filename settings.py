import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

DISCORD_PREFIX = os.environ.get("discord_prefix")
DISCORD_TOKEN = os.environ.get("discord_token")

YOUTUBE_KEY = os.environ.get("youtube_key")
YOUTUBE_ID = os.environ.get("youtube_id")
YOUTUBE_SECRET = os.environ.get("youtube_secret")

SPOTIFY_ID = os.environ.get("spotify_id")
SPOTIFY_SECRET = os.environ.get("spotify_secret")
