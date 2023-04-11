import discord
from discord.ext import commands

class Tuttu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tuttu(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("Oyunun oynanacağı kanalı belirtin.")
        channel_msg = await self.bot.wait_for("message", check=check)

        try:
            channel = await commands.TextChannelConverter().convert(ctx, channel_msg.content)
        except commands.ChannelNotFound:  # Hata adı düzeltildi
            await ctx.send("Kanal bulunamadı.")
            return
        
        def check_tuttu_tutmadı(message):
            return message.author != self.bot.user and message.channel == channel

        await ctx.send("Oyun başladı. Kanalda biri `tuttu` dediğinde ✅, `tutmadı` dediğinde ❌ reaksiyonları eklenecektir.")
        
        while True:
            try:
                message = await self.bot.wait_for("message", check=check_tuttu_tutmadı)
            except:
                return
            
            if "tuttu" in message.content.lower():
                await message.add_reaction("✅")
            elif "tutmadı" in message.content.lower():
                await message.add_reaction("❌")