import discord
from redbot.core import commands
import random

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_word = ""
        self.remaining_guesses = 0
        self.guessed_word = ""
        self.guessed_letters = []

    def start_game(self, word, guesses):
        self.current_word = word
        self.remaining_guesses = guesses
        self.guessed_word = "_" * len(self.current_word)
        self.guessed_letters = []

    def guess(self, guess):
        if guess.isalpha() and len(guess) == 1:
            guess = guess.lower()
            if guess in self.guessed_letters:
                return "You already guessed that letter."
            elif guess in self.current_word:
                for i in range(len(self.current_word)):
                    if guess == self.current_word[i]:
                        self.guessed_word = self.guessed_word[:i] + guess + self.guessed_word[i + 1:]
                self.guessed_letters.append(guess)
                if "_" not in self.guessed_word:
                    return "Congratulations, you guessed the word!"
                else:
                    return "Correct! " + self.guessed_word
            else:
                self.remaining_guesses -= 1
                self.guessed_letters.append(guess)
                if self.remaining_guesses == 0:
                    return "Game over. The word was " + self.current_word
                else:
                    return "Incorrect. You have " + str(self.remaining_guesses) + " guesses remaining."
        else:
            return "Invalid guess. Please enter a single letter."

    @commands.command()
    async def startgame(self, ctx, word: str, guesses: int):
        if guesses <= 0:
            await ctx.send("Invalid number of guesses.")
            return
        self.start_game(word.lower(), guesses)
        await ctx.author.send("The game has started! You have " + str(guesses) + " guesses. Here's the word: " + " ".join(list(self.guessed_word)))
        await ctx.send("The game has started in DMs!")
        
    @commands.command()
    async def guessword(self, ctx, guess: str):
        result = self.guess(guess.lower())
        if "_" not in self.guessed_word:
            await ctx.author.send(result)
            await ctx.send(result)
            self.current_word = ""
            self.remaining_guesses = 0
            self.guessed_word = ""
            self.guessed_letters = []
        else:
            word_display = " ".join([char if char != "_" else " " for char in self.guessed_word])
            if " " not in word_display:
                word_display = " ".join([char for char in self.guessed_word])
            await ctx.author.send(word_display)
            await ctx.author.send(result)
            await ctx.send(result)

    @guessword.error
    async def guessword_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a guess.")
        else:
            await ctx.send("Invalid guess. Please enter a single letter.")