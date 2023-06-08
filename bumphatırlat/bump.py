import asyncio
from redbot.core import commands
import discord
class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash = SlashCommand(bot, sync_commands=True)
        self.last_bump_time = None

        @self.slash.slash(name="bump")
        async def _bump(ctx: SlashContext):
            await self.bump(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() == "/bump":
            await self.bump(message)

    async def bump(self, ctx):
        disboard_bot_id = 302050872383242240  # DISBOARD botunun ID'si
        bump_channel = ctx.channel

        def check_bump_success(m):
            return str(m.author.id) == str(disboard_bot_id) and "Bump done" in m.content

        try:
            bump_success_msg = await self.bot.wait_for("message", check=check_bump_success, timeout=10)
            if bump_success_msg:
                self.last_bump_time = asyncio.get_event_loop().time()
                await bump_channel.send("Sunucunuz başarıyla bump yapıldı!")
        except asyncio.TimeoutError:
            pass

    @commands.command()
    async def nezamanbump(self, ctx):
        if self.last_bump_time is None:
            await ctx.send("Henüz hiç bump yapılmamış.")
        else:
            elapsed_time = asyncio.get_event_loop().time() - self.last_bump_time
            remaining_time = 7200 - elapsed_time
            if remaining_time <= 0:
                await ctx.send("Artık sunucunuzu bump yapabilirsiniz!")
            else:
                hours, remainder = divmod(int(remaining_time), 3600)
                minutes, seconds = divmod(remainder, 60)
                if hours > 0:
                    time_str = f"{hours} saat {minutes} dakika"
                elif minutes > 0:
                    time_str = f"{minutes} dakika {seconds} saniye"
                else:
                    time_str = f"{seconds} saniye"
                await ctx.send(f"Sunucunuzu tekrar bump yapmak için {time_str} beklemeniz gerekiyor.")
