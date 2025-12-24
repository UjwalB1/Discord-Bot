import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

base_dir = os.path.dirname(os.path.abspath(__file__)) # each time I run, the discord.log file no longer be outside expected dir
log_path = os.path.join(base_dir, "discord.log")
handler = logging.FileHandler(filename=log_path, encoding ="utf-8", mode = 'w')

class UjiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="uji ", intents=intents)

    # load cogs before bot connects
    async def setup_hook(self):
        cogs_path = os.path.join(base_dir, "cogs")
        for filename in os.listdir(cogs_path): 
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()
        print("global sync for slash commands fr")

bot = UjiBot()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

