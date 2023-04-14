# -*- coding: utf-8 -*-
from .say import Say

def setup(bot):
    bot.add_cog(Say(bot))