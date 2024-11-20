import discord
from discord.ext import commands

from settings import DISCORD_PREFIX
from commands import Misc

class ApolloBot(commands.Bot):
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=DISCORD_PREFIX,
            intents=intents,
            description="ApolloBot"
        )

    async def setup_hook(self):
        """
        Async setup hook that runs before the bot starts.

        This is where we load our cogs and perform any necessary async initialization.
        """
        await self.add_cog(Misc(self))
