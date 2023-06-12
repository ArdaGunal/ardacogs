from redbot.core import commands
import discord

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: discord.TextChannel = None,words *, message: str):
        if channel is None:
            channel=ctx.channel
            await ctx.send(message)
            await ctx.message.delete()
        else:
            await channel.send(message)
            await ctx.message.delete()
