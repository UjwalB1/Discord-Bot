import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot




    @commands.command(name="temporary_mute", aliases=["tm", "tempm", "tmute", "timeout"])
    @commands.has_permissions(mute_members=True)
    async def temp_mute(self, ctx, member: discord.Member, time_amount: int, duration_type: str, *, reason: str = None): #apparently * makes it greedy
        if reason is None:
            reason = "no reason was given"
            
        # convert to expected duration type 
        if duration_type.lower() == "s":
            duration = datetime.timedelta(seconds=time_amount)
        elif duration_type.lower() == "m":
            duration = datetime.timedelta(minutes=time_amount)
        elif duration_type.lower() == "h":
            duration = datetime.timedelta(hours=time_amount)
        elif duration_type.lower() == "d":
            duration = datetime.timedelta(days=time_amount)
        else:
            await ctx.send("Error: Duration type must be s, m, h, or d")
            return
        
        # check if person being tm'd is already tm'd
        if member.is_timed_out():
            await ctx.send(f"{member.mention} is already temp muted")
            return
        

        try:
            await member.timeout(duration, reason=reason)
            # shows all details after temp muting
            embed_tm = discord.Embed(title="Temp mute", description=f"{member.mention} has been muted", colour=discord.Colour.purple(), timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed_tm.add_field(name="Reason:", value=reason, inline=False)
            embed_tm.add_field(name="Duration:", value=f"{time_amount}{duration_type}", inline=False)
            await ctx.reply(embed=embed_tm )
            
        except discord.Forbidden:
            await ctx.send("I don't have permission to timeout members.")



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            reason = f"no reason was given for being kicked from {ctx.message.guild.name}"
        else:
            reason = reason + f", you've been kicked from {ctx.message.guild.name}"

        try:
            embed_kick = discord.Embed(title="Kick", description=f"{member.mention} has been kicked!", colour=discord.Colour.red(), timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed_kick.add_field(name="Reason:", value=reason, inline=False)
            embed_kick.set_thumbnail(url=member.display_avatar.url)
            await ctx.reply(embed=embed_kick)
            
            await member.send(embed=embed_kick)
            await member.kick()
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick members.")





    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.Member, *, reason: str = None):
        if reason is None:
            reason = f"no reason was given for being banned from {ctx.message.guild.name}"
        else:
            reason = reason + f", you've been banned from {ctx.message.guild.name}"

        try:
            embed_kick = discord.Embed(title="ban", description=f"{member.mention} has been banned!?", colour=discord.Colour.dark_red(), timestamp=datetime.datetime.now(datetime.timezone.utc))
            embed_kick.add_field(name="Reason:", value=reason, inline=False)
            embed_kick.set_thumbnail(url=member.display_avatar.url)
            await ctx.reply(embed=embed_kick)
            
            await member.send(embed=embed_kick)
            await member.ban()
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members.")





async def setup(bot):
    await bot.add_cog(Moderation(bot))