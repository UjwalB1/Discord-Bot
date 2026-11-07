import json
import logging
import os

import discord
from discord.ext import commands

SETTINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "welcome_channel.json")

log = logging.getLogger(__name__)


def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {}
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=4)


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="set_welcome", aliases=["sw", "setw", "setupw"], description="Set the channel for welcome messages.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel):
        data = load_settings()
        data[str(ctx.guild.id)] = channel.id
        save_settings(data)
        await ctx.send(f"Welcome channel set to {channel.mention}.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel_id = load_settings().get(str(guild.id))

        # saved channel first, then the system channel, then any channel the bot can post in
        candidates = [guild.get_channel(channel_id) if channel_id else None, guild.system_channel, *guild.text_channels]
        channel = next((c for c in candidates if c and c.permissions_for(guild.me).send_messages), None)
        if channel is None:
            log.warning("No channel to welcome %s in %s", member, guild.name)
            return

        embed = discord.Embed(title="Welcome!", description=f"Welcome to the server, {member.mention}!", color=discord.Color.green())
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
