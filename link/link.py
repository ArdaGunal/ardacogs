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
        replaced = False

        # Check if the message contains "www.instagram.com" and replace it
        if "www.instagram.com" in modified_content:
            modified_content = modified_content.replace("www.instagram.com", "www.ddinstagram.com")
            replaced = True
        
        # Check if the message contains "x.com" and replace it
        if "x.com" in modified_content:
            modified_content = modified_content.replace("x.com", "fixupx.com")
            replaced = True

        # If any replacements were made, send the modified message, delete the original, and mention the sender
        if replaced:
            await message.delete()
            new_message = f"**{message.author.display_name}:** {modified_content}"
            await message.channel.send(new_message)

def setup(bot):
    bot.add_cog(Link(bot))
