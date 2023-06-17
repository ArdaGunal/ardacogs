# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from random import choice
import asyncio

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_active = False
        self.word = ""
        self.guesses = []
        self.lives = 0
        self.game_channel = None
        self.game_start_time = None

    @commands.command()
    async def başla(self, ctx):
        if self.game_active:
            await ctx.send("Zaten bir oyun devam ediyor.")
            return

        self.game_active = True
        self.game_channel = ctx.channel
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
        self.game_start_time = discord.utils.utcnow()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.game_active or message.author.bot or message.channel != self.game_channel:
            return

        # Ignore command messages
        if message.content.startswith('.'):
            return

        # Wait for 3 seconds after the game starts before processing messages
        if (discord.utils.utcnow() - self.game_start_time).total_seconds() < 3:
            return

        guess = message.content.lower()
        correct_guess = False
        if len(guess) == 1:
            for i, c in enumerate(self.word):
                if c == guess:
                    self.guesses[i] = c
                    correct_guess = True
        else:
            if guess in self.word:
                start_index = self.word.index(guess)
                for i, c in enumerate(guess):
                    self.guesses[start_index + i] = c
                correct_guess = True

        if "".join(self.guesses) == self.word:
            await message.channel.send("Tebrikler! Kelimeyi doğru tahmin ettiniz: " + self.word)
            self.game_active = False
            return

        if not correct_guess:
            self.lives -= 1

        if self.lives <= 0:
            await message.channel.send("Kaybettiniz! Doğru kelime: " + self.word)
            self.game_active = False
            return

        await message.channel.send("Güncel durum: " + "".join(self.guesses) + f" (Kalan hak: {self.lives})")
