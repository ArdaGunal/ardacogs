from .merhaba import merhaba

async def setup(bot):
    bot.add_cog(merhaba(bot))
