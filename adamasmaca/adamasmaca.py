import random
import discord
from redbot.core import commands

class AdamAsmaca(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words = []

    @commands.command(name="adamasmaca")
    async def adamasmaca(self, ctx):
        """
        Adam Asmaca Oyunu
        """
        # Kelime listesini dosyadan yükleyin
        if not self.words:
            with open("kelimeler.txt", "r", encoding="utf-8") as file:
                self.words = file.read().splitlines()

        # Rastgele kelime seçin
        word = random.choice(self.words)

        # Oyun başlatın
        game_over = False
        incorrect_guesses = 0
        correct_guesses = set()
        while not game_over:
            # Kelimeyi gösterin
            word_display = ""
            for letter in word:
                if letter in correct_guesses:
                    word_display += f"{letter} "
                else:
                    word_display += "_ "

            await ctx.send(f"Kelime: {word_display}")

            # Tahmin alın
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            guess = await self.bot.wait_for("message", check=check)

            if guess.content == word:
                await ctx.send("Tebrikler, kelimeyi buldunuz!")
                game_over = True
            elif len(guess.content) == 1 and guess.content.isalpha():
                if guess.content in correct_guesses:
                    await ctx.send("Bu harfi zaten tahmin ettiniz!")
                elif guess.content in word:
                    correct_guesses.add(guess.content)
                    await ctx.send("Bu harf doğru!")
                    if len(correct_guesses) == len(set(word)):
                        await ctx.send("Tebrikler, kelimeyi buldunuz!")
                        game_over = True
                else:
                    incorrect_guesses += 1
                    await ctx.send(f"Bu harf yanlış! {6-incorrect_guesses} canınız kaldı!")
                    if incorrect_guesses == 6:
                        await ctx.send(f"Oyun bitti! Kelime: {word}")
                        game_over = True
            else:
                await ctx.send("Geçersiz tahmin! Tek bir harf veya tam kelime tahmin edin.")
        
    @commands.command(name="puan")
    async def puan(self, ctx):
        """
        Oyuncuların puanlarını gösterin
        """
        # TODO: Puan listesi gösterme işlemleri
        
    @commands.command(name="puan_ver")
    async def puan_ver(self, ctx, member: discord.Member, points: int):
        """
        Bir oyuncuya puan verin
        """
        # TODO: Oyuncuya puan verme işlemleri


def setup(bot):
    bot.add_cog(AdamAsmaca(bot))
