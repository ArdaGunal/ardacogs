import discord
from redbot.core import commands
import random

class Kelime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_word = ""
        self.guesses = set()

    @commands.hybrid_command(name="kelimeoyunu")
    async def kelimeoyunu(self, ctx):
        author = ctx.author
        dm_channel = await author.create_dm()
        await dm_channel.send("Lütfen bir kelime yazın, bu kelimeyi diğer oyuncular tahmin edecek.")
        def check(m):
            return m.author == author and isinstance(m.channel, discord.DMChannel)
        message = await self.bot.wait_for('message', check=check)
        self.current_word = message.content.lower()
        await ctx.send(f"{author.mention} tarafından seçilen kelime: {self.current_word}")
        self.guesses.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):
            return
        if self.current_word == "":
            return
        if message.content.lower() == self.current_word:
            await message.channel.send(f"Tebrikler, {message.author.mention} kelimeyi doğru bildiniz!")
            self.current_word = ""
            return
        if message.content.lower() in self.guesses:
            return
        self.guesses.add(message.content.lower())
        word_progress = []
        for letter in self.current_word:
            if letter.lower() in self.guesses:
                word_progress.append(letter)
            else:
                word_progress.append("_")
        await message.channel.send(f"{message.author.mention} tarafından yapılan tahmin: {' '.join(word_progress)}")

        if "_" not in word_progress:
            await message.channel.send(f"Tebrikler, {message.author.mention} kelimeyi doğru bildiniz!")
            self.current_word = ""

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, discord.Forbidden):
            await ctx.send("Kelime oyunu DM'den oynandığı için, sizinle özel mesaj yoluyla iletişim kuramıyorum. Lütfen DM'leri açın veya botu engellemeyin.")
        else:
            await ctx.send(f"Bir hata oluştu: {error}")
        self.current_word = ""
        self.guesses.clear()