# -*- coding: utf-8 -*-
from .SavedMessages import savedMessages

def setup(bot):
    bot.add_cog(savedMessages(bot))
    
    