# -*- coding: utf-8 -*-

    # -*- coding: utf-8 -*-
from .tahmin import Tahmin

async def setup(bot):

    cog = Tahmin(bot)

    await bot.add_cog(cog)