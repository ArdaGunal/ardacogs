import discord
from redbot.core import commands

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = None
        self.hidden_word = None
        self.guesses_left = None
        self.in_progress = False

    @commands.command(name="startgame")
    async def start_game(self, ctx):
        if self.in_progress:
            await ctx.send("There's already a game in progress!")
            return

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        await ctx.send("Let's start a new game! Please choose a word or a phrase.")
        msg = await self.bot.wait_for("message", check=check)
        self.word = msg.content.lower()

        if len(self.word) == 0:
            await ctx.send("The word or phrase must contain at least one character.")
            return

        await ctx.send("How many guesses do you want to allow?")
        msg = await self.bot.wait_for("message", check=check)

        try:
            self.guesses_left = int(msg.content)
        except ValueError:
            await ctx.send("Invalid input. Please enter a positive integer.")
            return

        if self.guesses_left <= 0:
            await ctx.send("The number of guesses must be positive.")
            return

        self.hidden_word = ["_" if c.isalpha() or c.isdigit() else c for c in self.word]
        self.in_progress = True

        await ctx.send("The game has started! The word or phrase is: " + " ".join(self.hidden_word))

    @commands.command(name="guess")
    async def guess(self, ctx, *, guess):
        if not self.in_progress:
            await ctx.send("No game is currently in progress.")
            return

        guess = guess.lower()

        if len(guess) != 1 and guess != self.word:
            await ctx.send("Invalid guess. Please guess exactly one letter or the entire word/phrase.")
            return

        if guess == self.word:
            self.hidden_word = list(self.word)
        else:
            if guess not in self.word:
                self.guesses_left -= 1

            for i, c in enumerate(self.word):
                if c == guess:
                    self.hidden_word[i] = guess

        if self.guesses_left == 0:
            await ctx.send("You lost! The word or phrase was: " + self.word)
            self.in_progress = False
            return

        if "_" not in self.hidden_word:
            await ctx.send("Congratulations, you won! The word or phrase was: " + self.word)
            self.in_progress = False
            return

        await ctx.send(" ".join(self.hidden_word))
        await ctx.send(f"You have {self.guesses_left} guess(es) left.")