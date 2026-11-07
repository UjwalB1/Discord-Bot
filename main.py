import logging
import math
import os
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))
TOKEN = os.getenv("DISCORD_TOKEN")

log = logging.getLogger("uji")


class UjiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="uji ", intents=intents)

    async def setup_hook(self):
        # every file in cogs/ is loaded as a feature module
        for filename in sorted(os.listdir(os.path.join(BASE_DIR, "cogs"))):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.CommandNotFound, commands.NotOwner)):
            return

        if isinstance(error, commands.CommandOnCooldown):
            minutes = math.ceil(error.retry_after / 60)
            await ctx.send(f"On cooldown, try again in {minutes} min.", ephemeral=True)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            missing = ", ".join(p.replace("_", " ") for p in error.missing_permissions)
            await ctx.send(f"I'm missing permissions: {missing}.", ephemeral=True)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only works in a server.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send(f"Usage: `{ctx.clean_prefix}{ctx.command.qualified_name} {ctx.command.signature}`", ephemeral=True)
        else:
            log.error("Error in command %s", ctx.command, exc_info=error)
            await ctx.send("Something went wrong, try again later.", ephemeral=True)


bot = UjiBot()


@bot.command()
@commands.is_owner()
async def sync(ctx):
    # register slash commands with Discord; run after adding or changing commands
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} slash commands.")


if __name__ == "__main__":
    handler = RotatingFileHandler(os.path.join(BASE_DIR, "discord.log"), maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    bot.run(TOKEN, log_handler=handler, log_level=logging.INFO, root_logger=True)
