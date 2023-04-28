# -*- coding: utf-8 -*-
from .tahmin import tahminoyun

def setup(bot):
    bot.add_cog(tahminoyun(bot))
    
    