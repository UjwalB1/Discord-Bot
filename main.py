import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
handler = logging.FileHandler(filename="discord.log", encoding ="utf-8", mode = 'w')

class UjiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="uji ", intents=intents)

    # load cogs before bot connects
    async def setup_c(self):
        for filename in os.listdir("./cogs"): 
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

bot = UjiBot()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

