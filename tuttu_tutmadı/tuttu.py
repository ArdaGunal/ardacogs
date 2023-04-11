from redbot.core import commands, checks, Config
import discord

class Tuttu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.active = False

    @commands.group()
    async def tuttu(self, ctx):
        """Tuttu tutmadı oyununu başlatır."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @tuttu.command(name="kanal")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Oyunun oynanacağı kanalı belirtir."""
        self.channel = channel
        await ctx.send(f"Oyun kanalı {channel.mention} olarak belirlendi.")

    @tuttu.command(name="başla")
    async def start_game(self, ctx):
        """Oyunu başlatır."""
        if self.channel is None:
            await ctx.send("Oyunun oynanacağı kanalı belirlemediniz.")
            return
        self.active = True
        await self.channel.send("Oyun başladı. Kanalda biri tuttu dediğinde ✅, tutmadı dediğinde ❌ reaksiyonları eklenecektir.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.active or message.channel != self.channel or message.author.bot:
            return

        content = message.content.lower().casefold()
        if "tuttu" in content:
            await message.add_reaction("✅")
        elif "tutmadı" in content:
            await message.add_reaction("❌")