# -*- coding: utf-8 -*-
from .say import Say

async def setup(bot):

    cog = Say(bot)

    await bot.add_cog(cog)