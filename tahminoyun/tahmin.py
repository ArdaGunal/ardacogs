import discord
from redbot.core import commands
import random

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = None
        self.guesses_left = None
        self.word_guessed = None

    @commands.command(name='startgame')
    async def start_game(self, ctx, channel: discord.TextChannel = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.author.dm_channel

        if not channel:
            channel = ctx.channel

        await ctx.author.send("Merhaba! Lütfen oyun için bir kelime veya cümle seçin.")
        msg = await self.bot.wait_for('message', check=check)

        await ctx.author.send("Kaç tahmin hakkı istersiniz?")
        guesses_left_msg = await self.bot.wait_for('message', check=check)

        word = msg.content.lower()
        word_guessed = ['-' if c.isalpha() else c for c in word]
        guesses_left = int(guesses_left_msg.content)

        await ctx.author.send(f"Kelimeniz: {' '.join(word_guessed)}")
        await ctx.author.send(f"{guesses_left} tahmin hakkınız var.")

        self.word = word
        self.guesses_left = guesses_left
        self.word_guessed = word_guessed

        await channel.send(f" {ctx.author.mention} kelime seçti ve oyun başladı.Tahminlerinizi alalım.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.isalpha() or message.author == self.bot.user:
            return

        if message.content.lower() == self.word:
            await message.channel.send(f"Tebrikler, {message.author.name}! Kelimeyi/cümleyi doğru tahmin ettiniz.")
            self.word_guessed = list(self.word)
            self.word = None
            self.guesses_left = None
            return

        if message.content.lower() in self.word:
            indexes = [i for i, c in enumerate(self.word) if c == message.content.lower()]
            for index in indexes:
                self.word_guessed[index] = message.content.lower()

            if '-' not in self.word_guessed:
                await message.channel.send(f"Tebrikler, {message.author.name}! Kelimeyi/cümleyi doğru tahmin ettiniz.")
                self.word = None
                self.guesses_left = None
                return

            await message.channel.send(f"{message.author.name} doğru harf tahmininde bulundunuz! {''.join(self.word_guessed)}")
        else:
            self.guesses_left -= 1
            if self.guesses_left <= 0:
                await message.channel.send(f"Oyunu kaybettiniz! Kelime/cümle '{self.word}' idi.")
                self.word = None
                self.guesses_left = None
                return

            await message.channel.send(f"{message.author.mention} yanlış harf tahmininde bulundunuz. Kalan tahmin hakkınız: {self.guesses_left} {''.join(self.word_guessed)}")