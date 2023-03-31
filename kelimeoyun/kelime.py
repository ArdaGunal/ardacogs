import discord
from redbot.core import commands
import random

class Kelime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sorular = ["anahtar", "bilgisayar", "kalem", "telefon", "evren", "köpek", "uçak", "araba", "balık", "muzik", "kitap", "yazılım", "insan", "çikolata", "güneş", "ay", "yıldız", "dünya", "okul", "deniz", "dağ", "şarkı", "film", "spor", "yemek", "tatil", "para", "saat", "gözlük", "tişört", "mont", "bot", "ayakkabı", "gökyüzü", "orman", "şehir", "kırsal", "yol", "tren", "yelkenli", "gemi", "köprü", "şifre", "kedi", "kuş", "fare", "zürafa", "fil", "kaplumbağa", "örümcek", "at", "yılan", "aslan", "balina", "penguen", "kanguru", "koyun", "inek", "horoz", "tavşan", "kelebek", "arı", "karınca", "örnek"]
        self.current_word = ""
        self.guesses = set()

    @commands.command(name="kelimeoyunu")
    async def kelimeoyunu(self, ctx):
        self.current_word = random.choice(self.sorular)
        await ctx.author.send("Kelime seçildi. Tahminlerinizi buradan yazabilirsiniz.")
        self.guesses.clear()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not isinstance(message.channel, discord.DMChannel):
            return
        if self.current_word == "":
            return
        if message.content.lower() == self.current_word:
            await message.author.send("Tebrikler, kelimeyi doğru bildiniz!")
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
        await message.author.send(" ".join(word_progress))

        if "_" not in word_progress:
            await message.author.send("Tebrikler, kelimeyi doğru bildiniz!")
            self.current_word = ""

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError) and isinstance(error.original, discord.Forbidden):
            await ctx.author.send("Kelime oyunu DM'den oynandığı için, sizinle özel mesaj yoluyla iletişim kuramıyorum. Lütfen DM'leri açın veya botu engellemeyin.")
        else:
            await ctx.author.send(f"Bir hata oluştu: {error}")
        self.current_word = ""
        self.guesses.clear()