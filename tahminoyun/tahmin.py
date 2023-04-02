import discord
from discord.ext import commands

class TahminOyun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        
    @commands.command()
    async def startgame(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == dm_channel

        dm_channel = await ctx.author.create_dm()
        await dm_channel.send("Kelime seçin:")
        message = await self.bot.wait_for("message", check=check)

        await dm_channel.send("Tahmin hakkınızı belirleyin:")
        message2 = await self.bot.wait_for("message", check=check)

        word = message.content.lower()
        num_tries = int(message2.content)

        hidden_word = ["_"] * len(word)

        embed = discord.Embed(title="Tahmin Oyunu", description=f"Kelime: {' '.join(hidden_word)}\nTahmin Hakkı: {num_tries}")
        msg = await ctx.send(embed=embed)

        game = {"word": word, "num_tries": num_tries, "hidden_word": hidden_word, "msg": msg, "guessed_letters": []}
        self.active_games[ctx.channel.id] = game

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id not in self.active_games:
            return

        game = self.active_games[message.channel.id]

        if message.content.lower() == game["word"]:
            await message.channel.send("Tebrikler, kazandınız!")
            self.active_games.pop(message.channel.id)
            return

        if message.content.lower() in game["guessed_letters"]:
            return

        if message.content.lower() not in game["word"]:
            game["num_tries"] -= 1
            if game["num_tries"] == 0:
                await message.channel.send(f"Hakkınız bitti! Kelime: {game['word']}")
                self.active_games.pop(message.channel.id)
                return
            await game["msg"].edit(embed=discord.Embed(title="Tahmin Oyunu", description=f"Kelime: {' '.join(game['hidden_word'])}\nTahmin Hakkı: {game['num_tries']}"))

        else:
            guess = message.content.lower()
            for i, letter in enumerate(game["word"]):
                if letter == guess:
                    game["hidden_word"][i] = guess

            game["guessed_letters"].append(guess)
            if "_" not in game["hidden_word"]:
                await message.channel.send("Tebrikler, kazandınız!")
                self.active_games.pop(message.channel.id)
                return

            await game["msg"].edit(embed=discord.Embed(title="Tahmin Oyunu", description=f"Kelime: {' '.join(game['hidden_word'])}\nTahmin Hakkı: {game['num_tries']}"))