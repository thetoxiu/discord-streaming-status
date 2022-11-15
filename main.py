import json
import discord
from discord.ext import commands

bot = commands.Bot(description="thetoxiu's streaming selfbot", command_prefix=",", self_bot=True)
bot.remove_command('help')


@bot.event
async def on_connect():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.streaming,
            url="https://twitch.tv/something",  # u can replace something with anything u want
            name="@toxiu.me"))  # text after Streaming ...


with open('./config.json') as f:
    config = json.load(f)

token = config.get('token')

bot.run(token)
