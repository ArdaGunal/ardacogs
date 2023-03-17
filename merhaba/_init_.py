from .merhaba import merhaba

async def setup(bot):
    bot.add_cog(merhabaCog(bot))
