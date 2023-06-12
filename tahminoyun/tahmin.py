import discord
from discord.ext import commands
from random import choice

class HangmanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_active = False
        self.word = ""
        self.guesses = []
        self.lives = 0

    @commands.command()
    async def başla(self, ctx):
        if self.game_active:
            await ctx.send("Zaten bir oyun devam ediyor.")
            return

        self.game_active = True
        await ctx.author.send("Kelime ya da cümlenizi girin:")
        def check(m):
            return m.author == ctx.author and m.channel == m.author.dm_channel
        word_message = await self.bot.wait_for('message', check=check)
        self.word = word_message.content.lower()

        await ctx.author.send("Oyunculara kaç hak vermek istiyorsunuz?")
        lives_message = await self.bot.wait_for('message', check=check)
        self.lives = int(lives_message.content)

        self.guesses = ["-" if c != " " else " " for c in self.word]
        await ctx.send("Oyun başladı! İlk durum: " + "".join(self.guesses))

    @commands.command()
    async def tahmin(self, ctx, guess: str):
        if not self.game_active:
            await ctx.send("Oyun başlamadı. Lütfen önce `!başla` komutunu kullanın.")
            return

        guess = guess.lower()
        if len(guess) == 1:
            for i, c in enumerate(self.word):
                if c == guess:
                    self.guesses[i] = c
        else:
            if guess == self.word:
                self.guesses = list(self.word)

        if "".join(self.guesses) == self.word:
            await ctx.send("Tebrikler! Kelimeyi doğru tahmin ettiniz: " + self.word)
            self.game_active = False
            return

        self.lives -= 1
        if self.lives <= 0:
            await ctx.send("Kaybettiniz! Doğru kelime: " + self.word)
            self.game_active = False
            return

        await ctx.send("Güncel durum: " + "".join(self.guesses) + f" (Kalan hak: {self.lives})")

def setup(bot):
    bot.add_cog(HangmanCog(bot))
