# -*- coding: utf-8 -*-
from .link import Link

async def setup(bot):

    cog = Link(bot)

    await bot.add_cog(cog)
