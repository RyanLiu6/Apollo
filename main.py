#!/usr/bin/env python3

import os
import threading

from flask import Flask

from bot import ApolloBot
from utils import setup_logging
from settings import DISCORD_TOKEN

# Create Flask app for health check
app = Flask(__name__)

@app.route("/health_check")
def health_check():
    return "Bot is running!", 200

def run_flask():
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))
    if os.environ.get("ENVIRONMENT") == "prod":
        # In production, Gunicorn will handle the app directly
        # This function won't be called
        pass
    else:
        app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Configure logging first
    setup_logging()

    # Start Flask in a separate thread if not in production
    if os.environ.get("ENVIRONMENT") != "prod":
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

    # Create and run the bot
    apollo_bot = ApolloBot()
    apollo_bot.run(DISCORD_TOKEN)
