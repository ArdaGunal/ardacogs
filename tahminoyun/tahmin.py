import discord
from redbot.core import commands
import asyncio
import random

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startgame(self, ctx):
        await ctx.send("Oyun başlatılıyor, lütfen özel mesajlarınızı kontrol edin.")
        await asyncio.sleep(1)
        await ctx.message.delete()

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        await ctx.author.send("Lütfen oynamak istediğiniz kelimeyi ya da cümleyi yazın:")
        kelime = await self.bot.wait_for('message', check=check)

        await ctx.author.send("Kaç tahmin hakkı istersiniz?")
        haklar = await self.bot.wait_for('message', check=check)

        kelime = kelime.content.lower()
        haklar = int(haklar.content)

        hidden_word = ["_" if c.isalnum() else c for c in kelime]

        embed = discord.Embed(title="Tahmin Oyunu", description=" ".join(hidden_word))
        msg = await ctx.send(embed=embed)

        while haklar > 0 and "_" in hidden_word:
            guess = await self.bot.wait_for('message', check=lambda m: m.author != self.bot.user and m.channel == ctx.channel)
            guess = guess.content.lower()

            if guess == kelime:
                await ctx.send(f"Tebrikler, doğru tahmin! Kelime: {kelime}")
                return

            if guess in kelime:
                for i, c in enumerate(kelime):
                    if c == guess:
                        hidden_word[i] = guess

                embed = discord.Embed(title="Tahmin Oyunu", description=" ".join(hidden_word))
                await msg.edit(embed=embed)

            else:
                haklar -= 1
                await ctx.send(f"Yanlış tahmin. Kalan hakkınız: {haklar}")

        if haklar == 0:
            await ctx.send(f"Maalesef hakkınız bitti. Doğru kelime: {kelime}")

    @startgame.error
    async def startgame_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Lütfen oynamak istediğiniz kanalda `startgame` komutunu kullanın.")