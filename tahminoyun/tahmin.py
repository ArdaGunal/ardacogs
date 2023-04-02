import random
from redbot.core import commands

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = ""
        self.hidden_word = []
        self.guesses = []
        self.max_guesses = 0
        self.current_guesses = 0

    @commands.command()
    async def startgame(self, ctx):
        await ctx.send("Oyunu başlatmak için lütfen özelden bir kelime seçin.")
        def check_word(msg):
            return msg.author == ctx.author and msg.channel == ctx.author.dm_channel
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check_word)
        except:
            await ctx.send("Kelime seçimi zaman aşımına uğradı.")
            return
        self.word = msg.content.lower()
        self.hidden_word = ["_"] * len(self.word)

        await ctx.send("Oyunu kaç tahmin hakkı ile oynamak istersiniz?")
        def check_guesses(msg):
            return msg.author == ctx.author and msg.channel == ctx.author.dm_channel
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check_guesses)
        except:
            await ctx.send("Tahmin hakkı seçimi zaman aşımına uğradı.")
            return
        self.max_guesses = int(msg.content)

        await ctx.send("Oyun başlıyor!")
        await ctx.send(" ".join(self.hidden_word))

    @commands.command()
    async def guess(self, ctx, guess):
        if not self.word:
            await ctx.send("Oyun henüz başlamadı.")
            return

        if len(guess) != 1:
            await ctx.send("Sadece bir harf girmelisiniz.")
            return

        guess = guess.lower()
        if guess in self.guesses:
            await ctx.send("Bu harfi zaten tahmin ettiniz.")
            return

        self.guesses.append(guess)
        if guess in self.word:
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    self.hidden_word[i] = guess
            await ctx.send(" ".join(self.hidden_word))
            if "_" not in self.hidden_word:
                await ctx.send("Tebrikler! Kelimeyi doğru tahmin ettiniz.")
                self.word = ""
                self.hidden_word = []
                self.guesses = []
                self.max_guesses = 0
                self.current_guesses = 0
            return

        self.current_guesses += 1
        if self.current_guesses >= self.max_guesses:
            await ctx.send("Tahmin hakkınız bitti. Kaybettiniz.")
            self.word = ""
            self.hidden_word = []
            self.guesses = []
            self.max_guesses = 0
            self.current_guesses = 0
            return

        await ctx.send(f"{guess} harfi kelimenin içinde değil. {self.max_guesses - self.current_guesses} tahmin hakkınız kaldı.")