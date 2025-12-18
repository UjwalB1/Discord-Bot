import discord
from discord.ext import commands
import os
import json

class General(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We are ready to go in, {self.bot.user.name}")


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        server_id = ctx.guild.id
        await ctx.send(f"Welcome channel has been set to{channel.mention}")



    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_id = member.guild.id
        channel = discord.utils.get(member.guild.channels, name="general")

        if channel:
            await channel.send(f"Welcome to the server {member.mention}!")






async def setup(bot):
    await bot.add_cog(General(bot))

