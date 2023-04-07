
import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import requests
class Burc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def get_burc_yorum(self, burc):
        url = f"https://www.elle.com.tr/astroloji/{burc}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        burc_yorumu = soup.find("div", class_="body-el-text standard-body-el-text").get_text().strip()

        return burc_yorumu
    @commands.command(name="burçyorum")
    async def burc_yorum(self, ctx, burc):
        burc = burc.lower()
        burc_yorumu = await self.get_burc_yorum(burc)
        await ctx.send(f"{burc.capitalize()} burcu günlük yorumu: {burc_yorumu}")

    