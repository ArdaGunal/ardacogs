import discord
from redbot.core import commands

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_game = None

    @commands.command(name='startgame')
    async def start_game(self, ctx):
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        await ctx.author.send("Oyunu başlatmak için bir kelime veya cümle seçin:")
        message = await self.bot.wait_for('message', check=check)
        word = message.content.lower()

        await ctx.author.send("Oyunda kaç tahmin hakkı olacak?")
        message = await self.bot.wait_for('message', check=check)
        try:
            num_guesses = int(message.content)
        except ValueError:
            await ctx.author.send("Lütfen geçerli bir sayı girin.")
            return

        hidden_word = "_ " * len(word) if " " not in word else "___ " * word.count(" ")
        await ctx.send(f"Oyun başladı! Kelime: {hidden_word}")

        def game_check(m):
            return m.channel == ctx.channel and m.author != self.bot.user

        guesses = []
        num_turns = 0

        while num_turns < num_guesses:
            message = await self.bot.wait_for('message', check=game_check)
            guess = message.content.lower()
            if guess in guesses:
                await ctx.send("Bu harfi/ kelimeyi zaten tahmin ettiniz.")
                continue
            guesses.append(guess)

            if guess == word:
                await ctx.send(f"{message.author.mention} tebrikler! Kelimeyi doğru tahmin ettiniz!")
                return
            elif len(guess) == len(word):
                num_turns += 1
                await ctx.send(f"{message.author.mention} yanlış tahmin. {num_guesses - num_turns} tahmin hakkınız kaldı.")
                continue

            if guess in word:
                indices = [i for i, letter in enumerate(word) if letter == guess]
                hidden_word = hidden_word.split()
                for i in indices:
                    hidden_word[i] = guess
                hidden_word = " ".join(hidden_word)
                if hidden_word.replace(" ", "") == word:
                    await ctx.send(f"{message.author.mention} tebrikler! Kelimeyi doğru tahmin ettiniz!")
                    return
                await ctx.send(f"{message.author.mention} doğru harf tahmini! {hidden_word}")
            else:
                num_turns += 1
                await ctx.send(f"{message.author.mention} yanlış tahmin. {num_guesses - num_turns} tahmin hakkınız kaldı. {hidden_word}")
        await ctx.send("Tahmin hakkınız kalmadı! Kaybettiniz.")
