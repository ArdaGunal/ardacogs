# -*- coding: utf-8 -*-
from .tahmin import Tahmin

def setup(bot):
    bot.add_cog(Tahmin(bot))
    
    