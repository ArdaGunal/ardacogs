from .bump import Bump

async def setup(bot):

    cog = Bump(bot)

    await bot.add_cog(cog)