import discord
from discord.ext import commands

class RequestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='request', help='Sunucu sahibine farklı isteklerde bulunmanızı sağlar')
    async def request(self, ctx, *, message):
        owner = ctx.guild.owner
        try:
            await owner.send(message)
            await ctx.send('Sunucu sahibine isteğiniz başarıyla gönderildi.')
        except:
            await ctx.send('Sunucu sahibine isteğiniz gönderilemedi.')

def setup(bot):
    bot.add_cog(RequestCog(bot))