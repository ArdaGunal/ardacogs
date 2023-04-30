# -*- coding: utf-8 -*-
from .cekilis import Cekilis

def setup(bot):
    bot.add_cog(Cekilis(bot))