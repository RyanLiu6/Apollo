#!/usr/bin/env python3

from settings import DISCORD_TOKEN
from bot import ApolloBot
from utils import setup_logging

if __name__ == "__main__":
    # Configure logging first
    setup_logging()
    
    # Create and run the bot
    apollo_bot = ApolloBot()
    apollo_bot.run(DISCORD_TOKEN)
