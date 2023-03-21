from .biyografi import biyografi

def setup(bot):
    bot.add_cog(biyografi(bot))