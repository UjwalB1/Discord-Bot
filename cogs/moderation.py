import datetime

import discord
from discord import app_commands
from discord.ext import commands

UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
MAX_TIMEOUT_SECONDS = 28 * 86400  # Discord's limit


def action_embed(title, member, colour, reason):
    embed = discord.Embed(title=title, description=f"{member.mention} has been {title.lower()}.", colour=colour, timestamp=discord.utils.utcnow())
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    return embed


async def notify(member, message, reason):
    # DM before removing them; closed DMs shouldn't stop the action
    try:
        await member.send(f"{message}\nReason: {reason}")
    except discord.HTTPException:
        pass


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def can_moderate(self, ctx, member):
        if member == ctx.author:
            await ctx.send("You can't do that to yourself.")
            return False
        if member.id == ctx.guild.owner_id or (ctx.author.id != ctx.guild.owner_id and member.top_role >= ctx.author.top_role):
            await ctx.send("You can't moderate someone with an equal or higher role.")
            return False
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("My role isn't high enough to do that.")
            return False
        return True

    @commands.hybrid_command(name="timeout", aliases=["tm", "tempm", "tmute", "temporary_mute"], description="Time out a member, e.g. 10 m.")
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @app_commands.describe(amount="How long, e.g. 10", unit="s, m, h, or d")
    async def timeout_member(self, ctx, member: discord.Member, amount: int, unit: str, *, reason: str = "No reason given"):
        unit = unit.lower()
        if unit not in UNIT_SECONDS or amount <= 0:
            await ctx.send("Duration must be a positive number followed by s, m, h, or d.")
            return

        seconds = amount * UNIT_SECONDS[unit]
        if seconds > MAX_TIMEOUT_SECONDS:
            await ctx.send("Timeouts can't be longer than 28 days.")
            return
        if member.is_timed_out():
            await ctx.send(f"{member.mention} is already timed out.")
            return
        if not await self.can_moderate(ctx, member):
            return

        await member.timeout(datetime.timedelta(seconds=seconds), reason=f"{ctx.author}: {reason}")
        embed = action_embed("Timed out", member, discord.Colour.purple(), reason)
        embed.add_field(name="Duration", value=f"{amount}{unit}", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Kick a member from the server.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
        if not await self.can_moderate(ctx, member):
            return

        await notify(member, f"You've been kicked from {ctx.guild.name}.", reason)
        await member.kick(reason=f"{ctx.author}: {reason}")
        await ctx.send(embed=action_embed("Kicked", member, discord.Colour.red(), reason))

    @commands.hybrid_command(description="Ban a member from the server.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason given"):
        if not await self.can_moderate(ctx, member):
            return

        await notify(member, f"You've been banned from {ctx.guild.name}.", reason)
        await member.ban(reason=f"{ctx.author}: {reason}")
        await ctx.send(embed=action_embed("Banned", member, discord.Colour.dark_red(), reason))


async def setup(bot):
    await bot.add_cog(Moderation(bot))
