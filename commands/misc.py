from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Misc(commands.Cog):
    """
    Miscellaneous commands and event handlers. Mainly responsible for utility and
    debugging commands that don't really quite fit into more specific categories.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Triggers once when the bot is ready and connected.
        """
        logger.info("ApolloBot is ready!")

    @commands.command(name="ping")
    async def pong(self, ctx):
        """
        Check the bot's latency. Responds with 'pong!' and the current latency. to Discord's servers.
        """
        logger.debug(f"Ping command executed by {ctx.author}")
        await ctx.send(f"pong! Latency: {round(self.bot.latency * 1000)}ms")
