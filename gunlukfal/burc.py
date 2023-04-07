from datetime import datetime
import pytz
import discord
from redbot.core import commands, tasks
from bs4 import BeautifulSoup
import requests


class Burc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.burclar = {
            "koç": "1", "boğa": "2", "ikizler": "3",
            "yengeç": "4", "aslan": "5", "başak": "6",
            "terazi": "7", "akrep": "8", "yay": "9",
            "oğlak": "10", "kova": "11", "balık": "12"
        }
        self.channel_id = 1048665677944336504
        self.timezone = 'Europe/Istanbul'
        self.prefix = "!"  # Burç Bot için kullanacağımız prefix

    async def get_burc_yorum(self, burc):
        url = f"https://onedio.com/gunluk-burc-yorumlari/{self.burclar[burc]}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        burc_yorumu = soup.find("div", class_="post-content").get_text().strip()

        return burc_yorumu

    @commands.command(name="burçyorum")
    async def burc_yorum(self, ctx, burc):
        burc = burc.lower()
        if burc not in self.burclar:
            await ctx.send("Geçersiz burç girdiniz!")
            return
        burc_yorumu = await self.get_burc_yorum(burc)
        await ctx.send(f"{burc.capitalize()} burcu günlük yorumu: {burc_yorumu}")

    @tasks.loop(hours=24)
    async def send_burc_yorum(self):
        now = datetime.now(pytz.timezone(self.timezone))
        if now.hour == 10 and now.minute == 0:
            channel = self.bot.get_channel(self.channel_id)
            for burc in self.burclar:
                burc_yorumu = await self.get_burc_yorum(burc)
                await channel.send(f"{burc.capitalize()} burcu günlük yorumu: {burc_yorumu}")

    @send_burc_yorum.before_loop
    async def before_send_burc_yorum(self):
        await self.bot.wait_until_ready()