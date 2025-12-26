import datetime
import discord
import os
from discord.ext import commands
from google import genai
from google.genai import types

class Summarizer(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))



    @commands.hybrid_command(name="summarize", description="Summarize last 200 messages in a channel (default: current), it will be goofy.")
    @commands.cooldown(1, 600, commands.BucketType.guild) # add cooldown so I don't use all my tokens rapidly
    async def summarize(self, ctx, channel: discord.TextChannel = None):
        await ctx.defer()
        
        if channel is None:
            channel = ctx.channel
        
        messages = []

        async for msg in channel.history(limit=200):
            if not msg.author.bot and msg.content:
                messages.append(f"{msg.author.display_name}: {msg.clean_content}") # ignore irrelevant messages n also format for gemini to understand stuff better

        messages.reverse()

        message_history = "\n".join(messages)

        prompt = f"You go by the name 'Uji bot,' and will summarize the message_history, in a non-serious joking manner, while still being concise and occassionally poke fun at certain things in the conversation and give opinions on it for jokes, REMEMBER TO KEEP RESPONSE RELATIVELY SHORT:\n\n {message_history}"

        response = self.client.models.generate_content( # gen the text output and hold it within the response var
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0) # disable thinking
            ),
        )

        embed_summarizer = discord.Embed(title="What you missed", description=response.text, colour=discord.Colour.blue(), timestamp=datetime.datetime.now(datetime.timezone.utc))

        await ctx.reply(embed = embed_summarizer)


    
    @summarize.error
    async def summarize_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"On cooldown from using the summarize feature, try again in a few minutes.", ephemeral=True) # only / command user sees message





async def setup(bot):
    await bot.add_cog(Summarizer(bot))