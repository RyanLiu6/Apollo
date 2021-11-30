import logging

from discord.ext import commands

from settings import TOKEN, PREFIX
from commands.secret_santa import make_secret_santas, get_secret_santa

logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger("Discord")
logger.setLevel(logging.WARNING)

bot = commands.Bot(command_prefix=PREFIX)

@bot.command(name="test")
async def test(ctx):
    logging.getLogger("Discord").info("INFO")
    logging.getLogger("Discord").debug("DEBUG")
    logging.getLogger("Discord").warning("WARN")

    logging.getLogger("Discord").warning(logging.getLogger("Discord").level)

    await ctx.send("Testing")

@bot.command(name="set_log_level")
async def set_log_level(ctx):
    options = ["INFO", "DEBUG", "WARN"]

    channel = ctx.message.channel
    content = ctx.message.content.split()

    if len(content) < 2:
        await channel.send(f"Malformed request, log level must be one of {options}")

    if content[1] not in options:
        await channel.send(f"Malformed request, log level must be one of {options}")
    else:
        if content[1] == options[0]:
            logging.getLogger("Discord").setLevel(logging.INFO)
        elif content[1] == options[1]:
            logging.getLogger("Discord").setLevel(logging.DEBUG)
        else:
            logging.getLogger("Discord").setLevel(logging.WARNING)

        await channel.send(f"Log level set to {content[1]}")

    logging.getLogger("Discord").warning(logging.getLogger("Discord").level)

@bot.command(name="secret_santa")
async def secret_santa(ctx):
    members = {}
    for item in ctx.message.mentions:
        members[item.name] = item.id

    secret_santas = make_secret_santas()
    secret_santas = get_secret_santa(year=2021)

    names = secret_santas.get_names()

    for name in names:
        uid = members[name]
        user = bot.get_user(uid)

        recipient = secret_santas.get_santa(name).recipient

        message = f"You are the Secret Santa to: {recipient}"

        logging.getLogger("Discord").debug(f"{name}, {message}")

        await user.send(message)

bot.run(TOKEN)
