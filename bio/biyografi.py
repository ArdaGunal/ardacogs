import discord
from redbot.core import commands

class Biyografi(commands.Cog):
    """Kullanıcılar için biyografi oluşturmayı ve düzenlemeyi sağlar"""

    def __init__(self, bot):
        self.bot = bot

    def get_biography(self, user_id):
        """Belirtilen kullanıcının biyografisini getirir"""
        return self.bot.db.get(f"biyografi:{user_id}", None)

    def save_biography(self, user_id, biography):
        """Belirtilen kullanıcının biyografisini kaydeder"""
        self.bot.db.put(f"biyografi:{user_id}", biography)

    def delete_biography(self, user_id):
        """Belirtilen kullanıcının biyografisini siler"""
        self.bot.db.delete(f"biyografi:{user_id}")

    @commands.command(name="bioekle")
    async def setbio(self, ctx, *, biyografi: str):
        """Biyografinizi kaydeder"""
        self.save_biography(ctx.author.id, biyografi)
        await ctx.send("Biyografiniz başarıyla kaydedildi.")

    @commands.command(name="biodüzenle")
    async def editbio(self, ctx, *, biyografi: str):
        """Mevcut biyografinizi düzenler"""
        if self.get_biography(ctx.author.id) is None:
            await ctx.send("Biyografiniz bulunamadı. Önce bir biyografi ekleyin.")
        else:
            self.save_biography(ctx.author.id, biyografi)
            await ctx.send("Biyografiniz başarıyla güncellendi.")

    @commands.command(name="biosil")
    async def deletebio(self, ctx):
        """Mevcut biyografinizi siler"""
        self.delete_biography(ctx.author.id)
        await ctx.send("Biyografiniz silindi")

    @commands.command(name="biyo")
    async def bio(self, ctx, kullanici: discord.Member = None):
        """Belirtilen kullanıcının biyografisini gösterir"""
        if kullanici is None:
            kullanici = ctx.author

        biyografi = await self.bot.db.get(f"biyografi:{kullanici.id}")

        if biyografi is None:
            await ctx.send("Bu kullanıcının biyografisi yok.")
        else:
            embed = discord.Embed(title=f"{kullanici.name} Biyografisi", description=biyografi, color=discord.Color.blue())
            await ctx.send(embed=embed)
