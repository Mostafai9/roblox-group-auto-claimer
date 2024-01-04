import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()

activity = discord.Game(name="MostafaAuto Claimer")
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

import AutoClaimerConfig

driver = asyncio.run(AutoClaimerConfig.get_driver())

@bot.event
async def on_ready():
    guild_count = len(bot.guilds)

    for guild in bot.guilds:
        print(f"- Guild ID: {guild.id} (Name: {guild.name})")

    print(f"Autoclaimer Started, Join my discord Server: https://discord.gg/2xdBsmyeak")

    await AutoClaimerConfig.Login(driver)

claimed = set()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)

    channels = [1162703145563062292, 951156423688077424] # put ur channel ids :D
    if message.channel.id in channels:
        if any(url in message.content for url in ('https://roblox.com', 'https://web.roblox.com')):
            links = [word for word in message.content.split() if word.startswith(('https://roblox.com', 'https://web.roblox.com'))]
            for link in links:
                print(f"Found a Group: {link}")

                await AutoClaimerConfig.JoinNClaimGroup(driver, link, message.channel)
                claimed.add(link)

@bot.command()
async def hello(ctx):
    await ctx.send("Hey Mostafa")

if __name__ == "__main__":
    bot.run("TOKEN HERE") # BOT TOKEN NOT DISCORD ACC TOKEN !!!
# dont forget to join my ds server bc why not
# https://discord.gg/2xdBsmyeak cool server fr
# or add me on dis user: o_0s