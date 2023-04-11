import discord
from redbot.core import commands
import random

class Tahmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word = None
        self.guesses_left = None
        self.word_guessed = None

   @commands.command(name='startgame')
async def start_game(self, ctx, channel: discord.TextChannel = None):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.author.dm_channel

    if not channel:
        channel = ctx.channel
    else:
        await ctx.author.send(f"Oyun kanalı olarak {channel.mention} seçildi.")
        
    await ctx.author.send("Merhaba! Lütfen oyun için bir kelime veya cümle seçin.")
    msg = await self.bot.wait_for('message', check=check)

    await ctx.author.send("Kaç tahmin hakkı istersiniz?")
    guesses_left_msg = await self.bot.wait_for('message', check=check)

    word = msg.content.lower()
    word_guessed = ['-' if c.isalpha() else c for c in word]
    guesses_left = int(guesses_left_msg.content)

    await ctx.author.send(f"Kelimeniz: {' '.join(word_guessed)}")
    await ctx.author.send(f"{guesses_left} tahmin hakkınız var.")

    self.word = word
    self.guesses_left = guesses_left
    self.word_guessed = word_guessed

    await channel.send(f" {ctx.author.mention} kelime seçti ve oyun başladı. Tahminlerinizi alalım.")