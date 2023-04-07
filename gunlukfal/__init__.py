# -*- coding: utf-8 -*-
from .burc import Burc

def setup(bot):
    bot.add_cog(Burc(bot))
    
    