
import discord
from redbot.core import commands
import asyncio

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot and "Öne çıkarma başarılı!" in message.embeds[0].title:
            channel = message.channel
            await channel.send("Tebrikler! Sunucuyu geliştirmeye yardımcı oldun.")
            await asyncio.sleep(10)  # 2 saat bekle (2 saat = 7200 saniye)
            await channel.send("Yeniden yazabilirsiniz! ")



    