from .bump import Bumpreminder

async def setup(bot):

    cog = Bumpreminder(bot)

    await bot.add_cog(cog)