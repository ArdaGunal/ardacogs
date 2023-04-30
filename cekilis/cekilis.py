import discord
from redbot.core import commands
import random
import asyncio

class Cekilis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx, time:int, prize:str):
        """Starts a giveaway in the current channel."""
        giveaway_embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"React with 🎉 to enter for a chance to win **{prize}**!",
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=giveaway_embed)
        await msg.add_reaction("🎉")

        await asyncio.sleep(time) # wait for the specified time

        msg = await ctx.channel.fetch_message(msg.id)
        users = await msg.reactions[0].users().flatten() # get all users who reacted
        users.pop(users.index(self.bot.user)) # remove the bot's reaction

        if len(users) > 0: # if there are users who entered
            winner = random.choice(users)
            winner_embed = discord.Embed(
                title="🎉 GIVEAWAY ENDED 🎉",
                description=f"Congratulations {winner.mention}! You won **{prize}**!",
                color=discord.Color.green()
            )
            await ctx.send(embed=winner_embed)
        else: # if no one entered
            no_winner_embed = discord.Embed(
                title="🎉 GIVEAWAY ENDED 🎉",
                description="No one entered the giveaway!",
                color=discord.Color.red()
            )
            await ctx.send(embed=no_winner_embed)
