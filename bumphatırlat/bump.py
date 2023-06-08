import asyncio
from redbot.core import commands

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() == "/bump":
            disboard_bot_id = "302050872383242240"  # DISBOARD botunun ID'si
            bump_channel = message.channel

            def check_bump_success(m):
                return m.author.id == disboard_bot_id and "Bump done" in m.content

            try:
                bump_success_msg = await self.bot.wait_for("message", check=check_bump_success, timeout=10)
                if bump_success_msg:
                    await asyncio.sleep(10)  # 2 saat bekle (2 * 60 * 60 saniye) 7200
                    await bump_channel.send("2 saat doldu, sunucuyu tekrar bump yapabilirsiniz!")
            except asyncio.TimeoutError:
                pass

