import discord
import random
import asyncio

from redbot.core import commands

class Cekilis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cekilis(self, ctx, kanal: discord.TextChannel, sure: str):
        """
        Bir çekiliş başlatır.
        Kanal: çekilişin yapıldığı kanal
        Süre: çekilişin ne kadar süreceği (örn. 5s, 10m, 1h, 1d)
        """
        sure_turu = sure[-1]  # son karakteri alın
        sure_miktari = int(sure[:-1])  # son karakter hariç tüm karakterleri alın ve integer'a çevirin

        # saniye, dakika, saat veya gün cinsinden çekiliş süresini hesaplayın
        if sure_turu == 's':
            sure_saniye = sure_miktari
        elif sure_turu == 'm':
            sure_saniye = sure_miktari * 60
        elif sure_turu == 'h':
            sure_saniye = sure_miktari * 60 * 60
        elif sure_turu == 'd':
            sure_saniye = sure_miktari * 60 * 60 * 24

        # çekiliş mesajını gönderin
        await ctx.send(f'🎉 {ctx.author.mention} tarafından başlatılan çekiliş {kanal.mention} kanalında {sure_miktari} {sure_turu} boyunca devam edecektir! 🎉')

        # belirtilen süre boyunca bekleyin
        await asyncio.sleep(sure_saniye)

        # kanaldaki mesajları alın
        messages = await kanal.history(limit=None).flatten()

        # sadece bot mesajlarını filtreleyin
        bot_messages = [message for message in messages if message.author == self.bot.user]

        # en az bir bot mesajı varsa
        if len(bot_messages) > 0:
            # kazanan mesajı rastgele seçin
            kazanan_mesaj = random.choice(bot_messages)

            # kazananın adını alın ve kazananı duyurun
            kazanan = kazanan_mesaj.author.mention
            await ctx.send(f'🎉 Tebrikler {kazanan}! 🎉')
        else:
            # bot mesajı yoksa, çekiliş sonuçlarını duyurun
            await ctx.send('Maalesef kimse çekilişi kazanamadı.')