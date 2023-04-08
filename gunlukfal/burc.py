# -*- coding: utf-8 -*-
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

    @commands.command(name="burç")
    async def burç(self, ctx, burc):
        member = ctx.author
        burc = burc.lower()
        burc_yorumu = await self.get_burc_yorum(burc)
        embed = discord.Embed(title=f"{member.display_name}'nin günlük falı", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=burc, value=burc_yorum )
        embed.set_image(url=https://i.elle.com.tr/elle-test-images/elle_{burc}.jpg(size=512))
        await ctx.send(embed=embed)

    
