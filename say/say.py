from redbot.core import commands

import discord

class Say(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command()

    async def say(self, ctx, channel: discord.TextChannel = None, *, message: str):

        if channel is None:

        message = message.replace(channel,'')

        else:

            await channel.send(message)

            await ctx.message.delete()

    
          

   
        
        
          
