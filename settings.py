import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Discord settings
DISCORD_PREFIX = os.environ.get("DISCORD_PREFIX")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_CONFIG_CHANNEL = "apollo-config"

# Reddit settings
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "script:apollo-discord-bot:v2.0.0"
