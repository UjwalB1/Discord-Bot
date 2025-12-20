import discord
import random
from discord.ext import commands
import os

class Gimmick(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot


    @commands.command(name = "8ball", aliases = ["8b"])
    async def eight_ball(self, ctx):
        responses = {
            'yes': ("Yes, of course!", "I am confident, YES.", "Yes, yes, yes yes!", "As much as I hate you, yes.", "Yea whatever twin"),
            'no': ("Definitely NOT.", "Just stop, no, NO.", "No, stop being delusional now", "NO, NO, NO!", "All love, but no."),
            'wildcards': ("Just shush, I don't care.", f"Get a job {ctx.author.mention}, you're UNEMPLOYED.", "You talk to bots with no thought process, lonely?", "I don't know, get a life", "We aren't friensd, stop talking to me")
        }
        
        rand = random.randint(0, 10)
        if rand <= 4:
            category = 'no'
        elif rand <= 9:
            category = 'yes'
        else:
            category = 'wildcards'
        
        final_response = random.choice(responses[category])
        
        eball_embed = discord.Embed(
            title="🎱 8-Ball",
            description=final_response,
            color = 0x3498db
        )
        eball_embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.reply(embed = eball_embed)









async def setup(bot):
    await bot.add_cog(Gimmick(bot))