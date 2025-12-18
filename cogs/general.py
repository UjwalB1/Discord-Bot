import discord
from discord.ext import commands
import os
import json

class General(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.welcome_channel_data = "welcome_channel.json"

        if not os.path.exists(self.welcome_channel_data):
            with open(self.welcome_channel_data, "w") as f:
                json.dump({}, f)


    def load_settings(self): # load json file fn to read
        with open(self.welcome_channel_data, "r") as f:
            return json.load(f)

    def save_settings(self, data): # savee json file fn to write new data/overwrite
        with open(self.welcome_channel_data, "w") as f:
            json.dump(data, f, indent=4)



    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot is ready to be deployed, war veteran bot dealing with randoms lol, {self.bot.user.name}")


    @commands.command(name="setWelcome")
    @commands.has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        data = self.load_settings()
        data[str(ctx.guild.id)] = channel.id
        self.save_settings(data)

        await ctx.send(f"Welcome channel has been set to {channel.mention}")



    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = self.load_settings()
        server_id = str(member.guild.id)
        target_channel = None

        if server_id in data:
            target_channel = self.bot.get_channel(int(data[server_id]))

        if not target_channel: # try system chan if the welcome channel hasn't been setup
            target_channel = member.guild.system_channel

        # final resort just use the first channel possible in the server
        if not target_channel:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    target_channel = channel
                    break


        if target_channel: # send message if valid channel found
            try:
                await target_channel.send(f"Welcome to the server {member.mention}!")
            except discord.Forbidden:
                print(f"Permission error in {member.guild.name}")






async def setup(bot):
    await bot.add_cog(General(bot))

