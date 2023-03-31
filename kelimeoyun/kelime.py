import discord
from redbot.core import commands
import random

class Kelime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_word = ""
        self.guesses = set()

    @commands.command(name="kelimeoyunu")
    async def kelimeoyunu(self, ctx):
        self.current_word = await ctx.author.send("Lütfen bir kelime yazın:")
        self.guesses.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.DMChannel):
            return
        if self.current_word == "":
            return

        if message.content.lower() == self.current_word.content.lower():
            await message.author.send("Tebrikler, kelimeyi doğru bildiniz!")
            self.current_word = ""
            return

        if len(message.content) == 1:
            if message.content.lower() in self.guesses:
                await message.author.send("Bu harfi zaten tahmin ettiniz.")
                return
            self.guesses.add(message.content.lower())
            if message.content.lower() in self.current_word.content.lower():
                word_progress = []
                for letter in self.current_word.content.lower():
                    if letter in self.guesses:
                        word_progress.append(letter)
                    else:
                        word_progress.append("_")
                await message.channel.send(f"{message.author.mention} harf doğru: {' '.join(word_progress)}")
            else:
                await message.channel.send(f"{message.author.mention} yanlış harf.")

        else:
            await message.channel.send(f"{message.author.mention} yanlış kelime.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, discord.Forbidden):
            await ctx.author.send("Kelime oyunu DM'den oynandığı için, sizinle özel mesaj yoluyla iletişim kuramıyorum. Lütfen DM'leri açın veya botu engellemeyin.")
        else:
            await ctx.author.send(f"Bir hata oluştu: {error}")
        self.current_word = ""
        self.guesses.clear()