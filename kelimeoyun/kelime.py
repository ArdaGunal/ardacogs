import discord
from discord.ext import commands

class Kelime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_word = ""
        self.guesses = set()

    @commands.command(name="kelimeoyunu")
    async def kelimeoyunu(self, ctx):
        await ctx.author.send("Kelimeyi DM'den yazın:")
        self.current_word = ""
        self.guesses.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not isinstance(message.channel, discord.DMChannel):
            return

        if self.current_word == "":
            self.current_word = message.content.lower()
            await message.author.send(f"Kelime seçildi: {self.current_word}. Tahminlerinizi kanala yazabilirsiniz.")
            return

        guess = message.content.lower()
        if guess == self.current_word:
            await message.channel.send(f"Tebrikler, {message.author.mention}! Kelimeyi doğru bildiniz!")
            self.current_word = ""
            self.guesses.clear()
            return

        if guess in self.guesses:
            await message.channel.send(f"{message.author.mention}, '{guess}' kelimesini zaten tahmin ettiniz!")
        else:
            self.guesses.add(guess)
            await message.channel.send(f"{message.author.mention}, '{guess}' kelimesi yanlış!")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, discord.Forbidden):
            await ctx.author.send("Kelime oyunu DM'den oynandığı için, sizinle özel mesaj yoluyla iletişim kuramıyorum. Lütfen DM'leri açın veya botu engellemeyin.")
        else:
            await ctx.author.send(f"Bir hata oluştu: {error}")
        self.current_word = ""
        self.guesses.clear()