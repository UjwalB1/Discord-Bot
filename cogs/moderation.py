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





async def setup(bot):
    await bot.add_cog(Moderation(bot))