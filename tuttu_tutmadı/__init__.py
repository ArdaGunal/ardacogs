# -*- coding: utf-8 -*-
from .tuttu import Tuttu

def setup(bot):
    bot.add_cog(Tuttu(bot))
    
    