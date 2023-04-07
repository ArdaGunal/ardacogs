# -*- coding: utf-8 -*-
import discord
import requests
from bs4 import BeautifulSoup
import re
from redbot.core import commands, tasks

class Burc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.burclar = ['Koç', 'Boğa', 'İkizler', 'Yengeç', 'Aslan', 'Başak', 'Terazi', 'Akrep', 'Yay', 'Oğlak', 'Kova', 'Balık']
        self.url = 'https://www.hurriyet.com.tr/astroloji/'

    def get_burc_yorumlari(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        yorumlar = soup.find_all('p', {'class': 'lead mb-5'})
        burc_yorumlari = {}
        for i, yorum in enumerate(yorumlar):
            burc_yorumlari[self.burclar[i]] = yorum.text
        return burc_yorumlari

    @commands.command(name='günlükburç', help='Günlük burç yorumlarını gösterir')
    async def show_gunluk_burc(self, ctx):
        burc_yorumlari = self.get_burc_yorumlari()
        embed = discord.Embed(title='Günlük Burç Yorumları', description='Bugünün burç yorumları:', color=0xff5733)
        for burc in self.burclar:
            embed.add_field(name=burc, value=burc_yorumlari[burc], inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='burcum', help='Kendi burcunuzun günlük yorumunu gösterir')
    async def show_burcum(self, ctx):
        author = str(ctx.message.author)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        burcum = soup.find('h2', {'class': 'sign-name'}).text.split()[0]
        yorum = soup.find('p', {'class': 'lead mb-5'}).text
        embed = discord.Embed(title='{} Burcu Günlük Yorumu'.format(burcum), description=yorum, color=0xff5733)
        await ctx.send(embed=embed)