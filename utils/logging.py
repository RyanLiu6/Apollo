import logging

def setup_logging():
    """
    Configure logging for the bot with proper formatting and log levels.

    This sets up:
    - Basic logging configuration with timestamps
    - Reduced noise from discord.py's internal loggers
    - Proper log format for better debugging
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    # Reduce noise from discord.py's own loggers
    discord_loggers = ["discord", "discord.http", "discord.gateway"]
    for logger_name in discord_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
