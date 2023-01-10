#!/usr/bin/env python3

import discord
import logging

from discord.ext import commands
from settings import DISCORD_PREFIX, DISCORD_TOKEN


apollo_bot = commands.Bot(command_prefix=DISCORD_PREFIX)


@apollo_bot.event
async def on_ready():
    print("ApolloBot is ready!")


@apollo_bot.command(name="test")
async def test(ctx):
    await ctx.send("Testing :woozy_face:")


@apollo_bot.command(name="ping")
async def pong(ctx):
    await ctx.send("pong")


@apollo_bot.command(name="set_log_level")
async def set_log_level(ctx):
    options = {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARN": logging.WARN,
    }

    channel = ctx.message.channel
    content = ctx.message.content.split()

    if len(content) < 2:
        await channel.send(f"Malformed request, log level must be one of {options.keys}")

    desired_log_level = content[1]
    if desired_log_level not in options.keys:
        await channel.send(f"Malformed request, log level must be one of {options.keys}")
    else:
        discord.utils.setup_logging(level=options[desired_log_level], root=False)

        await channel.send(f"Log level set to {desired_log_level}")


if __name__ == "__main__":
    discord.utils.setup_logging(level=logging.INFO, root=False)
    apollo_bot.run(DISCORD_TOKEN)
