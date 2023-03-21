from .biyografi import Biyografi

def setup(bot):
    bot.add_cog(Biyografi(bot))