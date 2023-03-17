from redbot.core import commands

class HelloCog(commands.Cog):
    """HelloCog - RedBot Cog Example"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Sends a hello message"""
        await ctx.send('Hello!')

def setup(bot):
    bot.add_cog(HelloCog(bot))
