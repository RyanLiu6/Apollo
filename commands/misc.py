import logging

from discord.ext import commands

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
    async def pong(self, ctx: commands.Context):
        """
        Check the bot's latency. Responds with "pong!" and the current latency. to Discord's servers.
        """
        logger.debug(f"Ping command executed by {ctx.author}")
        await ctx.send(f"pong! Latency: {round(self.bot.latency * 1000)}ms")

    @commands.command(name="checkperms")
    @commands.has_permissions(manage_channels=True)
    async def check_permissions(self, ctx: commands.Context):
        """
        Check the bot's permissions in the current channel and server.
        Requires manage_channels permission to use.
        """
        bot_member = ctx.guild.me
        channel_perms = ctx.channel.permissions_for(bot_member)
        server_perms = bot_member.guild_permissions

        # Create a formatted list of important permissions
        important_perms = {
            "manage_channels": "Manage Channels",
            "view_channel": "View Channels",
            "send_messages": "Send Messages",
            "manage_messages": "Manage Messages",
            "read_message_history": "Read Message History"
        }

        # Check channel permissions
        channel_status = []
        for perm_name, display_name in important_perms.items():
            has_perm = getattr(channel_perms, perm_name, False)
            status = "✅" if has_perm else "❌"
            channel_status.append(f"{status} {display_name}")

        # Check server permissions
        server_status = []
        for perm_name, display_name in important_perms.items():
            has_perm = getattr(server_perms, perm_name, False)
            status = "✅" if has_perm else "❌"
            server_status.append(f"{status} {display_name}")

        # Send the results
        await ctx.send(
            f"**Bot Permissions in #{ctx.channel.name}:**\n"
            + "\n".join(channel_status)
            + f"\n\n**Bot Permissions in {ctx.guild.name}:**\n"
            + "\n".join(server_status)
        )
