import discord
from discord.ext import commands

class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check if the message contains "www.instagram.com"
        if "www.instagram.com" in message.content:
            # Replace "www.instagram.com" with "www.ddinstagram.com"
            modified_content = message.content.replace("www.instagram.com", "www.ddinstagram.com")

            # Send the modified message
            await message.channel.send(modified_content)

def setup(bot):
    bot.add_cog(Link(bot))
