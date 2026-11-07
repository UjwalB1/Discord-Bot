import random

import discord
from discord.ext import commands

RESPONSES = {
    "yes": ("Yes, of course!", "I am confident, YES.", "Yes, yes, yes yes!", "As much as I hate you, yes.", "Yea whatever twin"),
    "no": ("Definitely NOT.", "Just stop, no, NO.", "No, stop being delusional now", "NO, NO, NO!", "All love, but no."),
    "wildcard": ("Just shush, I don't care.", "Ask me again after you touch some grass.", "I'm a bot, not a therapist.", "I don't know, figure it out yourself.", "Ask again later, I'm on break."),
}


class Gimmick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="8ball", aliases=["8b"], description="Ask the magic 8-ball a yes or no question.")
    async def eight_ball(self, ctx, *, question: str):
        category = random.choices(["yes", "no", "wildcard"], weights=[5, 5, 1])[0]

        embed = discord.Embed(title="🎱 8-Ball", description=f"**Q:** {question}\n**A:** {random.choice(RESPONSES[category])}", color=0x3498DB)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gimmick(bot))
