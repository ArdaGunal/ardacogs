from redbot.core import commands
import discord

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: discord.TextChannel = None, *message: str):
        message = ' '.join(message)
        if channel is None:
            await ctx.send(message)
        else:
            await channel.send(message)

