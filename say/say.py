from redbot.core import commands
import discord

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: discord.TextChannel = None, *, message: str):
        if not channel:
            channel = ctx.channel
        else:
            channel = discord.utils.get(ctx.guild.channels, id=channel.id)

        if channel:
            await channel.send(message)
            await ctx.message.delete()
        else:
            await ctx.send("Belirtilen kanal bulunamadı.")

