import discord
from redbot.core import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", pass_context=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        """Sends a message to a specified channel."""
        try:
            await channel.send(message)
        except discord.Forbidden:
            await ctx.send("I don't have permission to send messages in that channel.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(Say(bot))