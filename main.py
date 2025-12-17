import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding ='utf-8', mode = 'w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='uji ', intents = intents)

role_member = 'Member'



@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")


@bot.event
async def on_message(message):
    if message.author == bot.user: # don't enter a loop of a bot responding to itself
        return
    if "sigma" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} stop using brainrot!")
    
    await bot.process_commands(message)



@bot.command()
async def hello(ctx):
    await ctx.reply(f"Hello {ctx.author.mention}!")



@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = role_member)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned the role {role_member}")
    else:
        await ctx.send("Role doesn't exist")



@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name = role_member)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has removed the role {role_member}")
    else:
        await ctx.send("Role doesn't exist")




@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title = 'New Poll', description = question)
    await ctx.message.delete() # Delete the message which initiates the poll, so it looks nicer in chat
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")





@bot.command()
@commands.has_role(role_member)
async def secret(ctx):
    await ctx.send("Finally a member fr")
    

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")








bot.run(token, log_handler = handler, log_level=logging.DEBUG)