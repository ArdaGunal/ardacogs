import discord
from redbot.core import commands
import random

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = ""
        self.guesses = []
        self.max_attempts = 5
        self.current_attempts = 0
        self.win = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.lower() == "!startgame":
            await message.author.send("Lütfen bir kelime veya cümle seçin ve bana özel mesaj olarak gönderin.")
            self.guesses = []
            self.current_attempts = 0
            self.win = False

        elif message.content.lower() == "!endgame":
            await message.channel.send("Oyun iptal edildi.")
            self.word = ""
            self.guesses = []
            self.current_attempts = 0
            self.win = False

        elif message.content.lower() == "!guesses":
            await message.channel.send(f"Kalan tahmin hakkınız: {self.max_attempts - self.current_attempts}\nTahminleriniz: {', '.join(self.guesses)}")

        elif message.author == message.author.bot:
            return

        elif self.word == "":
            self.word = message.content.lower()
            if len(self.word.split()) > 1:
                await message.channel.send(f"Cümle seçildi. Toplam {len(self.word.split())} kelime ve {len(self.word)} harf var.")
                self.word = self.word.split()
            else:
                await message.channel.send(f"Kelime seçildi. Toplam {len(self.word)} harf var.")
                self.word = list(self.word)
            await message.channel.send("Oyuna başlandı. Tahminlerinizi yapabilirsiniz.")

        elif self.win:
            return

        else:
            guess = message.content.lower()
            if guess in self.guesses:
                await message.channel.send("Bu harfi/daha önce bu kelimeyi zaten tahmin ettiniz. Lütfen başka bir harf/kelime deneyin.")
            else:
                self.guesses.append(guess)
                if isinstance(self.word, list):
                    if guess == "".join(self.word):
                        await message.channel.send("Tebrikler! Doğru kelimeyi tahmin ettiniz.")
                        self.win = True
                    else:
                        await message.channel.send("Maalesef yanlış kelime tahmini. Lütfen tekrar deneyin.")
                else:
                    if guess in self.word:
                        await message.channel.send(f"Tebrikler! '{guess}' harfi doğru.")
                        if all(letter in self.guesses for letter in self.word):
                            await message.channel.send("Tebrikler! Tüm harfleri doğru tahmin ettiniz.")
                            self.win = True
                    else:
                        await message.channel.send(f"Maalesef '{guess}' harfi yanlış. Lütfen tekrar deneyin.")
                        self.current_attempts += 1
                        if self.current_attempts == self.max_attempts:
                            await message.channel.send("Maalesef tahmin hakkınız kalmadı. Kaybettiniz.")
                            self.word = ""
                            self.win = True