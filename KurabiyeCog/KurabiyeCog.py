import random
import discord
from redbot.core import commands

class KurabiyeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kurabiyeler = {}

    @commands.command(name='kurabiye', aliases=['k'])
    async def kurabiye(self, ctx):
        """
        Sunucuda bir kurabiye verir.
        """
        if ctx.author.id not in self.kurabiyeler:
            self.kurabiyeler[ctx.author.id] = 0
        
        self.kurabiyeler[ctx.author.id] += 1
        await ctx.send(f'{ctx.author.mention} bir kurabiye aldı! 🍪 Toplam kurabiye sayısı: {self.kurabiyeler[ctx.author.id]}')

    @commands.command(name='kurabiyesayısı', aliases=['ks'])
    async def kurabiyesayisi(self, ctx):
        """
        Kendi toplam kurabiye sayısını gösterir.
        """
        if ctx.author.id not in self.kurabiyeler:
            self.kurabiyeler[ctx.author.id] = 0
        
        await ctx.send(f'{ctx.author.mention}, toplam kurabiye sayın: {self.kurabiyeler[ctx.author.id]}')

    @commands.command(name='kurabiyeçal', aliases=['kc'])
    async def kurabiyecal(self, ctx, member: discord.Member):
        """
        Başka bir kullanıcının kurabiyelerini çalar.
        """
        if member.id == ctx.author.id:
            await ctx.send("Kendinden kurabiye çalamazsın! 😠")
            return
        
        if member.id not in self.kurabiyeler:
            self.kurabiyeler[member.id] = 0

        if self.kurabiyeler[member.id] < 1:
            await ctx.send(f"{member.mention} adlı kullanıcının hiç kurabiyesi yok! 🍪😢")
            return

        self.kurabiyeler[member.id] -= 1
        self.kurabiyeler[ctx.author.id] += 1

        await ctx.send(f"{ctx.author.mention} adlı kullanıcı {member.mention} adlı kullanıcıdan bir kurabiye çaldı! 🍪")

    @commands.command(name='kurabiyetoplam', aliases=['kt'])
    async def kurabiyetoplam(self, ctx):
        """
        Sunucudaki tüm kurabiye sayısını gösterir.
        """
        toplam_kurabiye = sum(self.kurabiyeler.values())
        await ctx.send(f'Sunucudaki toplam kurabiye sayısı: {toplam_kurabiye}')

    @commands.command(name='kurabiyesıfırla', aliases=['ksıfırla'])
    @commands.is_owner()
    async def kurabiyesisifirla(self, ctx):
        """
        Tüm kullanıcıların kurabiye sayısını sıfırlar.
        """
        self.kurabiyeler.clear()
        await ctx.send("Tüm kurabiyeler sıfırlandı! 🍪🍪🍪")
