import random
import discord
from redbot.core import commands

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = ["apple", "banana", "cherry", "date", "elderberry"]
        self.guesses = 7

    @commands.command()
    async def start(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.author.dm_channel

        word = random.choice(self.words)
        blanks = "_" * len(word)
        await ctx.author.send(f"Kelime: {blanks}\nTahmin hakkınız: {self.guesses}\nKelimeyi tahmin etmek için lütfen harf ya da kelime yazın.")

        while self.guesses > 0 and blanks != word:
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.author.send("Süreniz doldu, oyunu kaybettiniz!")
                return

            guess = msg.content.lower()
            if len(guess) == len(word) and guess == word:
                await ctx.send(f"{ctx.author.mention} kazandın! Kelime: {word}")
                return
            elif len(guess) == 1 and guess in word:
                indices = [i for i in range(len(word)) if word[i] == guess]
                for i in indices:
                    blanks = blanks[:i] + guess + blanks[i+1:]
                await ctx.author.send(f"Doğru! Kelime: {blanks}")
            else:
                self.guesses -= 1
                await ctx.author.send(f"Yanlış tahmin! Kalan tahmin hakkınız: {self.guesses}")
        if self.guesses == 0:
            await ctx.author.send(f"Maalesef tahmin hakkınız bitti! Doğru cevap: {word}")
        else:
            await ctx.send(f"{ctx.author.mention} kazandın! Kelime: {word}")