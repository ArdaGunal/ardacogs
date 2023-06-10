from redbot.core import commands
import discord

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *args):
        channel = None
        message = None

        if len(args) > 1 and isinstance(args[0], discord.TextChannel):
            channel = args[0]
            message = ' '.join(args[1:])
        else:
            message = ' '.join(args)

        if channel is None:
            await ctx.send(message)
        else:
            await channel.send(message)

def setup(bot):
    cog = SayCog(bot)
    bot.add_cog(cog)
