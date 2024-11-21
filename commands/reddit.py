import json
import logging
import discord
import asyncpraw
from datetime import datetime
from typing import Dict
from discord.ext import commands, tasks

from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, DISCORD_CONFIG_CHANNEL


logger = logging.getLogger(__name__)

class RedditClientError(Exception):
    pass

class Reddit(commands.Cog):
    """
    Reddit monitoring cog that watches subreddits and posts new posts to configured channels.

    Primary use-case for me personally is for sales!
    """
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        self.configs = {}
        self.time_threshold = datetime.utcnow()

        self._setup_reddit_client()
        self.monitor_task = self.monitor_subreddits.start()

    def _setup_reddit_client(self):
        if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
            raise RedditClientError("Reddit API credentials not found. Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in your .env file or configuration.")

        try:
            self.reddit = asyncpraw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT)

            logger.info("Reddit client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {str(e)}")
            raise RedditClientError(f"Failed to initialize Reddit client: {str(e)}")

    async def get_config_channel(self, guild: discord.Guild) -> discord.TextChannel:
        """
        Returns the configuration channel. If it doesn't exist yet, it will be created.

        Args:
            guild (discord.Guild): The guild to get config channel for.
                In Discord, a guild is a server.

        Returns:
            channel (discord.TextChannel): The config channel object.
        """
        # apollo-config (DISCORD_CONFIG_CHANNEL) is the default name for the config channel, and will exist as a private channel
        channel = discord.utils.get(guild.text_channels, name=DISCORD_CONFIG_CHANNEL)
        if not channel:
            # Create config channel with restricted permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }

            try:
                channel = await guild.create_text_channel(
                    DISCORD_CONFIG_CHANNEL,
                    overwrites=overwrites,
                    topic="Apollo Bot Configuration - Do not delete this channel!",
                    reason="Apollo Bot Configuration Channel"
                )
                logger.info(f"Created config channel in guild {guild.name}")
                return channel
            except discord.Forbidden:
                logger.error(f"Failed to create config channel in guild {guild.name} - Missing permissions")
                raise
            except Exception as e:
                logger.error(f"Failed to create config channel in guild {guild.name}: {str(e)}")
                raise
        return channel

    async def load_guild_config(self, guild_id: int) -> Dict:
        """
        Load guild (server) configuration from config channel. Configuration is loaded into memory as a dictionary.

        Args:
            guild_id (int): Guild ID of the guild to get config channel for.
                In Discord, a guild is a server.

        Returns:
            config (dict): Configuration for this given guild.
        """
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return {}

        channel = await self.get_config_channel(guild)
        config = {"channel_configs": {}}

        # Get pinned message containing config - should be first message
        pins = await channel.pins()
        config_message = next((m for m in pins if m.author == self.bot.user), None)

        if config_message:
            try:
                config = json.loads(config_message.content)
                logger.debug(f"Loaded config for guild {guild_id}")
            except json.JSONDecodeError:
                logger.error(f"Failed to parse config for guild {guild_id}")

        self.configs[guild_id] = config
        return config

    async def save_guild_config(self, guild_id: int, guild_config: Dict):
        """
        Saves guild (Server) configuration to config channel.

        Args:
            guild_id (int): Guild ID of the guild to get config channel for.
                In Discord, a guild is a server.
            guild_config (dict): Configuration for this given guild.
        """
        if guild_id not in self.configs:
            return

        channel = await self.get_config_channel(self.bot.get_guild(guild_id))
        config_str = json.dumps(guild_config, indent=2)

        # Update or create pinned config message - should be first message
        pins = await channel.pins()
        config_message = next((m for m in pins if m.author == self.bot.user), None)

        try:
            if config_message:
                await config_message.edit(content=config_str)
            else:
                message = await channel.send(content=config_str)
                await message.pin()
            logger.debug(f"Saved config for guild {guild_id}")
        except Exception as e:
            logger.error(f"Failed to save config for guild {guild_id}: {str(e)}")

    async def _get_config(self, guild: discord.Guild):
        """
        Helper function to ensure guild config is loaded.

        Args:
            guild (discord.Guild): The guild to get config channel for.
                In Discord, a guild is a server.

        Returns:
            guild_id, guild_config: The guild ID and guild configuration.
        """
        guild_id = guild.id
        if guild_id not in self.configs:
            await self.load_guild_config(guild_id)

        guild_config = self.configs[guild_id]

        return guild_id, guild_config

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """
        Setup config channel when Bot joins a new guild (server). In some cases, the Bot might have
        already joined the guild before, so we can also attempt to load the existing config.

        Args:
            guild (discord.Guild): The guild to get config channel for.
                In Discord, a guild is a server.
        """
        await self.get_config_channel(guild)
        await self.load_guild_config(guild.id)

    @commands.group(name="reddit")
    @commands.has_permissions(manage_channels=True)
    async def reddit(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand. Use !help reddit for more info.")

    @reddit.command(name="subscribe")
    async def subscribe(self, ctx: commands.Context, subreddit: str, *, filters: str = ""):
        """
        Subscribe to a subreddit with optional post filters. All updates post to this channel.
        Usage: !reddit subscribe bapcsales "gpu,cpu"

        Args:
            ctx (commands.Context): The context of the command invocation.
            subreddit (str): Subreddit to subscribe to.
            filters (str, optional): Filters to apply to posts. Defaults to "".
        """
        # Ensure config is loaded
        guild_id, guild_config = await self._get_config(ctx.guild)
        channel_id = str(ctx.channel.id)
        subreddit = subreddit.lower()

        # Clean up filters
        filters = filters.lower().strip()
        # Handle both ASCII and Unicode quotes
        for quote in ['"', "'", '\u201c', '\u201d']:  # straight quotes and Unicode smart quotes
            filters = filters.replace(quote, '')
        filters = [f.strip() for f in filters.split(",") if f.strip()]

        # Update config
        if "channel_configs" not in guild_config:
            guild_config["channel_configs"] = {}

        guild_config["channel_configs"][channel_id] = {
            "subreddit": subreddit,
            "filters": filters
        }

        await self.save_guild_config(guild_id, guild_config)

        # Format response message
        response = f"✅ Subscribed to r/{subreddit} in this channel ({ctx.channel.name})"
        if filters:
            filter_list = ", ".join(filters)
            response += f"\nFilters: {filter_list}"

        await ctx.send(response)

    @reddit.command(name="unsubscribe")
    async def unsubscribe(self, ctx: commands.Context):
        """
        Unsubscribe the current channel from Reddit updates.
        Usage: !reddit unsubscribe

        Args:
            ctx (commands.Context): The context of the command invocation.
        """
        # Ensure config is loaded
        guild_id, guild_config = await self._get_config(ctx.guild)
        channel_id = str(ctx.channel.id)

        if channel_id in guild_config.get("channel_configs", {}):
            del guild_config["channel_configs"][channel_id]
            await self.save_guild_config(guild_id, guild_config)
            await ctx.send(f"✅ Unsubscribed from Reddit updates in this channel ({ctx.channel.name})")
        else:
            await ctx.send(f"❌ This channel ({ctx.channel.name}) is not subscribed to any subreddit")

    @reddit.command(name="list")
    async def list_subscriptions(self, ctx: commands.Context):
        """
        List Reddit subscriptions for this channel.
        Usage: !reddit list

        Args:
            ctx (commands.Context): The context of the command invocation.
        """
        # Ensure config is loaded
        guild_id, guild_config = await self._get_config(ctx.guild)
        channel_id = str(ctx.channel.id)

        if channel_id in guild_config.get("channel_configs", {}):
            config = guild_config["channel_configs"][channel_id]
            filters_text = f"\nFilters: {', '.join(config['filters'])}" if config["filters"] else ""
            await ctx.send(f"📑 Subscribed to r/{config['subreddit']}{filters_text}")
        else:
            await ctx.send(f"❌ This channel ({ctx.channel.name}) is not subscribed to any subreddit")

    # Monitor subreddit task
    @tasks.loop(minutes=2.0)
    async def monitor_subreddits(self):
        """
        Monitors subreddits for new posts matching filters.
        Only posts newer than when the bot started will be processed.
        """
        try:
            # First, update time
            self.time_threshold = datetime.utcnow()

            for guild_id, guild_config in self.configs.items():
                for channel_id, config in guild_config.get("channel_configs", {}).items():
                    subreddit = config["subreddit"]
                    filters = config["filters"]

                    # Get the Discord channel
                    channel = self.bot.get_channel(int(channel_id))
                    if not channel:
                        continue

                    # Monitor the subreddit - only the 5 most recent posts
                    try:
                        subreddit_instance = await self.reddit.subreddit(subreddit)
                        async for submission in subreddit_instance.new(limit=5):
                            # Only process posts newer than when the bot started
                            submission_time = datetime.utcfromtimestamp(submission.created_utc)
                            if submission_time <= self.time_threshold:
                                continue

                            # Check if post matches any filters
                            if not filters or any(f.lower() in submission.title.lower() for f in filters):
                                embed = discord.Embed(
                                    title=submission.title,
                                    url=f"https://reddit.com{submission.permalink}",
                                    color=0xFF4500  # Reddit's orange color
                                )
                                embed.set_author(name=f"New post in r/{subreddit}")
                                await channel.send(embed=embed)
                    except Exception as e:
                        logger.error(f"Error monitoring r/{subreddit}: {str(e)}")

        except Exception as e:
            logger.error(f"Error in monitor task: {str(e)}")

    @monitor_subreddits.before_loop
    async def before_monitor(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.monitor_task.cancel()
