import re
import discord
from redbot.core import commands

class Tuttu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tuttu(self, ctx, channel: discord.TextChannel):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        def check_tuttu_tutmadı(reaction, user):
            return user != self.bot.user and reaction.message.channel == channel

       # await ctx.send("Oyun başladı. Kanalda biri `tuttu` dediğinde ✅, `tutmadı` dediğinde ❌ reaksiyonları eklenecektir.")

        while True:
            try:
                reaction, _ = await self.bot.wait_for("reaction_add", check=check_tuttu_tutmadı)
            except asyncio.TimeoutError:
                break

            if str(reaction.emoji) == "✅":
                await reaction.message.add_reaction("✅")
            elif str(reaction.emoji) == "❌":
                await reaction.message.add_reaction("❌")