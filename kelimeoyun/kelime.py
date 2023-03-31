import discord
from redbot.core import commands
import random

class Kelime(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  # Oyun başlatma komutu
  @commands.command()
  async def redbot(self, ctx):
    await ctx.author.send("Merhaba! Lütfen aşağıdaki kanalda tahmin edilmesi gereken kelimeyi girin: ")
    await ctx.send("Redbot oyunu başladı! Tahmin edilmesi gereken kelimeyi özelden " + ctx.author.mention + " yazacak.")

    def check(m):
      return m.channel == ctx.channel and m.author != self.bot.user

    # Tahmin edilecek kelimeyi özelden alın
    try:
      guesser = ctx.author
      guess = await self.bot.wait_for('message', check=check, timeout=60.0)
      word = guess.content.lower()
    except asyncio.TimeoutError:
      await ctx.send("Zaman aşımı! Oyun sona erdi.")
      return

    # Oyun başlat
    guessed_word = ["_" for _ in range(len(word))]
    guesses = set()
    attempts = 6

    while attempts > 0 and "_" in guessed_word:
      # Tahminleri kontrol et
      def guess_check(m):
        return m.channel == ctx.channel and m.author != self.bot.user and len(m.content) == 1 and m.content.isalpha()

      guess = await self.bot.wait_for('message', check=guess_check)
      guess = guess.content.lower()

      if guess in guesses:
        await ctx.send("Bu harfi zaten tahmin ettiniz!")
        continue
      else:
        guesses.add(guess)

      if guess in word:
        for i in range(len(word)):
          if word[i] == guess:
            guessed_word[i] = guess
        await ctx.send("Tahmininiz doğru! Tahmin ettiğiniz harf bu kelimenin içinde var.")
      else:
        attempts -= 1
        await ctx.send("Tahmininiz yanlış! Kalan hakkınız: " + str(attempts))

      await ctx.send("Tahmin edilen kelime: " + " ".join(guessed_word))

    if "_" not in guessed_word:
      await ctx.send("Tebrikler, kelimeyi doğru tahmin ettiniz!")
    else:
      await ctx.send("Üzgünüm, kelimeyi tahmin edemediniz. Doğru kelime: " + word)

