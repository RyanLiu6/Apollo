from discord.ext import commands

from settings import TOKEN, PREFIX
from commands.secret_santa import make_secret_santas, get_secret_santa

bot = commands.Bot(command_prefix=PREFIX)

@bot.command(name="test")
async def test(ctx):
    await ctx.send("Testing")

@bot.command(name="secret_santa")
async def secret_santa(ctx):
    mentions = ctx.message.mentions

    members = {}
    for item in mentions:
        members[item.name] = item.id

    # secret_santas = make_secret_santas()
    secret_santas = get_secret_santa(year=2020)

    names = secret_santas.get_names()

    print(secret_santas)

    for name in names:
        # uid = members[name]
        # user = bot.get_user(uid)

        recipient = secret_santas.get_santa(name).recipient

        message = f"You are the Secret Santa to: {recipient}"

        print(name, message)

        # await user.send()

bot.run(TOKEN)
