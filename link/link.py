import discord
from redbot.core import commands

class Link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        modified_content = message.content

        # Check if the message contains "www.instagram.com" and replace it
        if "www.instagram.com" in modified_content:
            modified_content = modified_content.replace("www.instagram.com", "www.ddinstagram.com")
        
        # Check if the message contains "x.com" and replace it
        if "x.com" in modified_content:
            modified_content = modified_content.replace("x.com", "fixupx.com")

        # Send the modified message if any replacements were made
        if modified_content != message.content:
            await message.channel.send(modified_content)

def setup(bot):
    bot.add_cog(Link(bot))
